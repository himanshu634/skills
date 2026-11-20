#!/usr/bin/env python3
"""Series locks: the frozen look of one series (bible + spec + series layer + engine copy).

Usage:
  lock.py pack --bible bible.md --spec spec.json --series series.js [--engine engine.js]
               [--status draft|approved] [--previous old-lock.md] --out LOCK.md
  lock.py check LOCK.md              integrity: hashes, contract, vocabulary
  lock.py unpack LOCK.md OUTDIR      bible.md, spec.json, series.js, engine.js, manifest.json
  lock.py shared LOCK.md             print the film's modules/shared.js (engine + series, verbatim)
  lock.py manifest LOCK.md           print the vocabulary (what scenes and briefs may name)
  lock.py instructions LOCK.md       print the project-instructions snippet
  lock.py diff OLD.md NEW.md         what changed between two versions

Needs node (to read the series layer's vocabulary without a browser).
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parent / "engine" / "engine.js"
VOCAB = ("light", "lens", "living", "cast", "sets")
MARK = "<!-- production-house:lock"

NODE = r"""
const vm = require('vm'), fs = require('fs'), crypto = require('crypto');
const [engine, series] = process.argv.slice(2).map(p => fs.readFileSync(p, 'utf8'));
let touched = null;
const doc = new Proxy({}, { get(_, k) { touched = touched || String(k); return () => ({ style: {}, setAttribute() {}, appendChild() {} }); } });
const ctx = { console, WeakMap, Map, Math, JSON, Object, Array, Number, String };
ctx.window = ctx; ctx.document = doc;
vm.createContext(ctx);
const out = { errors: [] };
try { vm.runInContext(engine, ctx); } catch (e) { out.errors.push('engine failed to load: ' + e.message); }
if (touched) out.errors.push('engine touches the DOM at load (' + touched + ')');
touched = null;
try { vm.runInContext(series, ctx); } catch (e) { out.errors.push('series layer failed to load: ' + e.message); }
if (touched) out.errors.push('series layer touches the DOM at load (document.' + touched + '); define functions only');
const h = s => crypto.createHash('sha256').update(String(s)).digest('hex').slice(0, 12);
const E = ctx.PH, S = ctx.SERIES;
out.engine_version = E && E.version;
if (!S) out.errors.push('series layer does not define window.SERIES');
else {
  out.id = S.id; out.version = S.version; out.engine = S.engine; out.look = S.look || null;
  out.vocab = {}; out.entries = {};
  for (const g of ['light', 'lens', 'living', 'cast', 'sets']) {
    const o = S[g] || {};
    out.vocab[g] = Object.keys(o).sort();
    for (const k of out.vocab[g]) {
      if (typeof o[k] !== 'function') out.errors.push(`SERIES.${g}.${k} is not a function`);
      out.entries[`${g}.${k}`] = h(o[k]);
    }
  }
  out.helpers = Object.keys(S).filter(k => typeof S[k] === 'function').sort();
  for (const k of out.helpers) out.entries[k] = h(S[k]);
  for (const k of ['frame', 'finish']) if (typeof S[k] !== 'function') out.errors.push(`SERIES.${k} is required (use a no-op if the look has none)`);
  if (!/^\d+\.\d+\.\d+$/.test(S.version || '')) out.errors.push('SERIES.version must be semver, e.g. 1.0.0');
  if (!/^[a-z][a-z0-9-]{1,40}$/.test(S.id || '')) out.errors.push('SERIES.id must be a lowercase slug');
  if (E && S.engine && String(E.version).split('.')[0] !== String(S.engine).split('.')[0]) out.errors.push(`series built for engine ${S.engine}, engine is ${E.version}`);
}
console.log(JSON.stringify(out));
"""


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def inspect(engine_src, series_src):
    with tempfile.TemporaryDirectory() as d:
        e, s, n = Path(d) / "e.js", Path(d) / "s.js", Path(d) / "n.js"
        e.write_text(engine_src); s.write_text(series_src); n.write_text(NODE)
        r = subprocess.run(["node", str(n), str(e), str(s)], capture_output=True, text=True)
    if r.returncode:
        sys.exit("node failed: " + r.stderr)
    return json.loads(r.stdout)


def fence(lang, body):
    return f"```{lang}\n{body.rstrip()}\n```"


def section(text, title):
    m = re.search(r"^## " + re.escape(title) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else None


def block(text, title, lang):
    sec = section(text, title)
    if sec is None:
        return None
    m = re.search(r"```" + lang + r"\n(.*?)\n```", sec, re.S)
    return m.group(1) + "\n" if m else None


def read(path):
    text = Path(path).read_text()
    if MARK not in text:
        sys.exit(f"{path} is not a Production House series lock")
    parts = {
        "bible": (section(text, "Bible") or "").strip() + "\n",
        "spec": json.loads(block(text, "Spec", "json")),
        "manifest": json.loads(block(text, "Manifest", "json")),
        "series": block(text, "Series layer", "js"),
        "engine": block(text, "Engine", "js"),
    }
    head = re.search(MARK + r"(.*?)-->", text, re.S).group(1)
    parts["status"] = (re.search(r"status (\S+)", head) or [None, "draft"])[1]
    return parts


def bump_kind(old, new):
    oe, ne = old["entries"], new["entries"]
    removed = sorted(set(oe) - set(ne))
    changed = sorted(k for k in set(oe) & set(ne) if oe[k] != ne[k])
    added = sorted(set(ne) - set(oe))
    return removed, changed, added


def ver(v):
    return tuple(int(x) for x in v.split("."))


def pack(a):
    bible, spec_txt, series = Path(a.bible).read_text(), Path(a.spec).read_text(), Path(a.series).read_text()
    engine = Path(a.engine).read_text() if a.engine else ENGINE.read_text()
    spec = json.loads(spec_txt)
    info = inspect(engine, series)
    errs = list(info["errors"])
    if spec.get("series") != info.get("id"):
        errs.append(f"spec.series '{spec.get('series')}' != SERIES.id '{info.get('id')}'")
    if spec.get("version") != info.get("version"):
        errs.append(f"spec.version '{spec.get('version')}' != SERIES.version '{info.get('version')}'")
    if a.previous and not errs:
        old = read(a.previous)
        om = old["manifest"]
        removed, changed, added = bump_kind(om, info)
        ov, nv = ver(om["version"]), ver(info["version"])
        text_changed = old["bible"].strip() != bible.strip() or old["spec"] != spec
        if om["engine_sha"] != sha(engine):
            changed.append("engine")
        if removed or changed:
            if nv[0] <= ov[0]:
                errs.append(f"existing vocabulary changed ({', '.join(removed + changed)}): a MAJOR bump is required "
                            f"({om['version']} -> {ov[0] + 1}.0.0), and the look must be re-approved")
        elif added:
            if nv <= ov or nv[0] != ov[0]:
                errs.append(f"vocabulary added ({', '.join(added)}): a MINOR bump is required ({om['version']} -> {ov[0]}.{ov[1] + 1}.0)")
        elif text_changed and nv <= ov:
            errs.append(f"bible or spec changed: a PATCH bump is required ({om['version']} -> {ov[0]}.{ov[1]}.{ov[2] + 1})")
    if errs:
        for e in errs:
            print("ERROR", e)
        sys.exit(1)
    manifest = {k: info[k] for k in ("id", "version", "engine_version", "look", "vocab", "helpers", "entries")}
    manifest["engine_sha"] = sha(engine)
    manifest["series_sha"] = sha(series)
    title = spec.get("title") or info["id"]
    out = "\n\n".join([
        f"# Series lock: {title} · v{info['version']}",
        f"{MARK} v1 · series {info['id']} · version {info['version']} · status {a.status} -->",
        "Keep this file in the project's files. Production House reads it before every film in this series and "
        "installs its code verbatim, so every episode shares one look. Change it only through a version bump "
        "(`lock.py pack --previous`), never by hand.",
        "## Bible\n\n" + bible.strip(),
        "## Spec\n\n" + fence("json", json.dumps(spec, indent=1, ensure_ascii=False)),
        "## Manifest (generated, do not edit)\n\n" + fence("json", json.dumps(manifest, indent=1, ensure_ascii=False)),
        "## Series layer\n\n" + fence("js", series),
        "## Engine (frozen copy, do not edit)\n\n" + fence("js", engine),
    ]) + "\n"
    Path(a.out).write_text(out)
    print(f"PACKED {a.out}: {info['id']} v{info['version']} ({a.status}), engine {info['engine_version']}, "
          + ", ".join(f"{g} {len(info['vocab'][g])}" for g in VOCAB))


def check(path, quiet=False):
    p = read(path)
    info = inspect(p["engine"], p["series"])
    m, errs = p["manifest"], list(info["errors"])
    if sha(p["engine"]) != m["engine_sha"]:
        errs.append("engine copy was edited after packing (hash mismatch)")
    if sha(p["series"]) != m["series_sha"]:
        errs.append("series layer was edited after packing (hash mismatch); repack with a version bump")
    if info.get("vocab") != m.get("vocab"):
        errs.append("manifest vocabulary does not match the series layer")
    if p["spec"].get("version") != m["version"]:
        errs.append("spec version does not match the manifest")
    if not quiet:
        for e in errs:
            print("ERROR", e)
        print(f"{'FAIL' if errs else 'PASS'}: {m['id']} v{m['version']} ({p['status']})")
    return errs, p


def shared(p):
    m = p["manifest"]
    return (f"/* shared.js for series {m['id']} v{m['version']} (lock status {p['status']}). Installed verbatim from the "
            f"series lock: engine {m['engine_sha']}, series {m['series_sha']}. Do not edit; bump the lock instead. */\n"
            + p["engine"] + "\n" + p["series"])


def instructions(path, p):
    m = p["manifest"]
    name = Path(path).name
    return (f"This project is the series \"{p['spec'].get('title', m['id'])}\". Its look is frozen in the series lock "
            f"`{name}` (v{m['version']}) in this project's files. For every film in this project: use the "
            f"production-house skill, load that lock first, install its shared.js verbatim, use only the vocabulary it "
            f"defines, and follow its bible. Don't change the look, characters or sets unless I ask for a version bump.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pk = sub.add_parser("pack")
    for k in ("bible", "spec", "series", "out"):
        pk.add_argument("--" + k, required=True)
    pk.add_argument("--engine")
    pk.add_argument("--status", default="draft", choices=["draft", "approved"])
    pk.add_argument("--previous")
    for c in ("check", "shared", "manifest", "instructions"):
        sub.add_parser(c).add_argument("lock")
    up = sub.add_parser("unpack"); up.add_argument("lock"); up.add_argument("out")
    df = sub.add_parser("diff"); df.add_argument("old"); df.add_argument("new")
    a = ap.parse_args()
    if a.cmd == "pack":
        return pack(a)
    if a.cmd == "check":
        errs, _ = check(a.lock)
        sys.exit(1 if errs else 0)
    if a.cmd == "diff":
        o, n = read(a.old), read(a.new)
        r, c, ad = bump_kind(o["manifest"], n["manifest"])
        print(f"{o['manifest']['version']} -> {n['manifest']['version']}")
        print("removed:", ", ".join(r) or "-"); print("changed:", ", ".join(c) or "-"); print("added:  ", ", ".join(ad) or "-")
        return
    errs, p = check(a.lock, quiet=True)
    if errs:
        sys.exit("lock fails its integrity check; run: lock.py check " + a.lock)
    if a.cmd == "shared":
        sys.stdout.write(shared(p))
    elif a.cmd == "manifest":
        print(json.dumps({"id": p["manifest"]["id"], "version": p["manifest"]["version"], "status": p["status"],
                          "vocab": p["manifest"]["vocab"], "helpers": p["manifest"]["helpers"]}, indent=1))
    elif a.cmd == "instructions":
        print(instructions(a.lock, p))
    elif a.cmd == "unpack":
        o = Path(a.out); o.mkdir(parents=True, exist_ok=True)
        (o / "bible.md").write_text(p["bible"])
        (o / "spec.json").write_text(json.dumps(p["spec"], indent=1, ensure_ascii=False))
        (o / "series.js").write_text(p["series"])
        (o / "engine.js").write_text(p["engine"])
        (o / "manifest.json").write_text(json.dumps(p["manifest"], indent=1))
        print(f"unpacked to {o}")


if __name__ == "__main__":
    main()
