#!/usr/bin/env python3
"""Lint a Motion film's modules: universal checks, then the series' own scene contract.

Input is a folder holding the film's modules, as raw files (scene-office.js, scenes.json,
base.css, shared.js) or as the JSON documents the Artifact tool saves with read_db + out_dir
(each {"kind", "text"}).

Usage:
  lint_scenes.py FOLDER --lock LOCK.md [--brief brief.json]
Exit 1 when any error is found.

Universal (every series):
  U1 modules     every scene in scenes.json has a module
  U2 budget      scene modules within Motion's size limit
  U3 durations   scene durations match the brief
  U4 determinism no Math.random, clocks, timers, CSS transitions
  U5 quoting     no quote nested inside style="..."
  U6 kit         shared.js is the lock's build, verbatim (this is what keeps a series consistent)
  U7 vocabulary  scenes only call recipes, modes, cast and sets the lock defines
  U8 palette     base.css colors are not only black, red and white/cream (unless the lock allows it)
  U9 gate        a draft lock shoots tone tests only
Series (from the lock's scene_contract): require, require_any, forbid, budgets, words.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
MOTION = json.loads((HERE / "motion.json").read_text())


def load_modules(folder):
    mods = {}
    for p in sorted(Path(folder).rglob("*")):
        if not p.is_file():
            continue
        name, text = p.name, None
        if p.suffix == ".json":
            try:
                doc = json.loads(p.read_text())
            except Exception:
                continue
            if isinstance(doc, dict):
                inner = doc.get("data") if isinstance(doc.get("data"), dict) else doc
                if "text" in inner and "kind" in inner:
                    text = inner["text"]
                    name = name[:-5] if name.count(".") > 1 else name
                elif "scenes" in doc:
                    text = json.dumps(doc)
        if text is None:
            text = p.read_text(errors="replace")
        mods[name] = text
    return mods


def words_on_screen(code):
    found = re.findall(r'class="[^"]*\b(?:line|sub|title|card|words)\b[^"]*"[^>]*>([^<]{1,300})<', code)
    return sum(len(x.split()) for x in found)


def norm(s):
    return s.replace("\r\n", "\n").strip()


def lint(folder, lk, brief=None):
    from brief import only_brw
    from lock import shared
    mods = load_modules(folder)
    errs, warns, info = [], [], []
    spec, man = lk["spec"], lk["manifest"]
    con, vocab = spec.get("scene_contract", {}), man["vocab"]
    scene_files = {k: v for k, v in mods.items() if re.match(r"scene-[a-z0-9-]+\.js$", k)}
    order, durs = None, {}
    if "scenes.json" in mods:
        try:
            sj = json.loads(mods["scenes.json"])
            order = [s["id"] for s in sj["scenes"]]
            durs = {s["id"]: float(s["dur"]) for s in sj["scenes"]}
        except Exception as e:
            errs.append(f"U1 scenes.json unreadable: {e}")
    if not scene_files:
        errs.append("U1 no scene-*.js modules found")
        return errs, warns, info
    ids = order or [k[6:-3] for k in scene_files]
    for k in scene_files:
        if order and k[6:-3] not in order:
            warns.append(f"U1 {k} is not listed in scenes.json")
    bscenes = {s["id"]: s for s in (brief or {}).get("scenes", [])}
    total = sum(durs.values()) if durs else sum(float(s.get("dur", 0)) for s in bscenes.values())
    counts = {}
    for i, sid in enumerate(ids):
        code, tag = scene_files.get(f"scene-{sid}.js"), f"[{sid}]"
        if code is None:
            errs.append(f"{tag} U1 listed in scenes.json but has no module")
            continue
        edge = i in (0, len(ids) - 1)
        n = len(code)
        if n > MOTION["max_scene_chars"]:
            errs.append(f"{tag} U2 {n} characters (Motion max {MOTION['max_scene_chars']})")
        elif n > MOTION["target_scene_chars"] * 1.4:
            warns.append(f"{tag} U2 {n} characters (target about {MOTION['target_scene_chars']}); move reusable art into the lock")
        if durs and sid in bscenes and abs(durs[sid] - float(bscenes[sid]["dur"])) > 0.1:
            errs.append(f"{tag} U3 dur {durs[sid]} differs from the brief's {bscenes[sid]['dur']}")
        for pat, why in ((r"Math\.random", "Math.random (use PH.rng or kit.rng)"),
                         (r"Date\.now|performance\.now|setTimeout|setInterval|requestAnimationFrame", "timers or clocks"),
                         (r"transition\s*:|animation\s*:", "CSS transitions or animations")):
            if re.search(pat, code):
                errs.append(f"{tag} U4 {why}")
        if re.search(r'style="[^"]*\'', code):
            errs.append(f"{tag} U5 a quote nested inside style=\"...\"")
        for g, k in re.findall(r"SERIES\.(light|lens|living|cast|sets)\.([A-Za-z_$][\w$]*)", code):
            if k not in vocab[g]:
                errs.append(f"{tag} U7 SERIES.{g}.{k} is not in the lock (has: {', '.join(vocab[g]) or 'none'}); "
                            f"add it in the art department with a version bump, don't invent it in a scene")
        for k in re.findall(r"SERIES\.([A-Za-z_$][\w$]*)\s*\(", code):
            if k not in man["helpers"]:
                errs.append(f"{tag} U7 SERIES.{k}() is not in the lock")
        for r in con.get("require", []):
            if r["call"] not in code:
                errs.append(f"{tag} series: missing {r['call']} ({r.get('why', '')})")
        for r in con.get("require_any", []):
            if not any(c in code for c in r["calls"]):
                errs.append(f"{tag} series: needs one of {r['calls']} ({r.get('why', '')})")
        for r in con.get("forbid", []):
            if re.search(r["pattern"], code) and not (r.get("unless") and bscenes.get(sid, {}).get(r["unless"])):
                errs.append(f"{tag} series: forbidden /{r['pattern']}/ ({r.get('why', '')})"
                            + (f"; mark the scene '{r['unless']}' in the brief if intended" if r.get("unless") else ""))
        for mode in vocab["lens"]:
            counts[mode] = counts.get(mode, 0) + len(re.findall(r"SERIES\.lens\." + re.escape(mode) + r"\s*\(", code))
        wc = words_on_screen(code)
        cap = con.get("max_words_per_scene", 12)
        if wc > cap and not edge:
            warns.append(f"{tag} series: {wc} words on screen (cap {cap})")
        info.append(f"{tag} {n} chars, words {wc}")
    for bud in con.get("budgets", []):
        mode = bud.get("lens_mode")
        if mode:
            cap = bud["per_film"] if "per_film" in bud else max(bud.get("min", 0), round(total / 60 * bud.get("per_60s", 1)))
            if counts.get(mode, 0) > cap:
                errs.append(f"series: lens '{mode}' used {counts[mode]}x; budget {cap} ({bud.get('why', '')})")
    want = shared(lk)
    if "shared.js" not in mods:
        errs.append(f"U6 no shared.js: install the lock's build verbatim (lock.py shared)")
    elif norm(mods["shared.js"]) != norm(want):
        got = hashlib.sha256(norm(mods["shared.js"]).encode()).hexdigest()[:12]
        errs.append(f"U6 shared.js is not the build of lock v{man['version']} (sha {got}); reinstall it verbatim, never edit it in the film")
    css = mods.get("base.css", "")
    cols = re.findall(r"--(?:ground|main|second|accent)\s*:\s*(#[0-9a-fA-F]{6})", css)
    if len(cols) == 4 and only_brw(cols) and not con.get("allow_black_red_white"):
        errs.append("U8 base.css palette reads as only black/red/white-cream")
    if lk["status"] != "approved" and (len(ids) > 2 or total > 15):
        errs.append(f"U9 lock v{man['version']} is a draft: shoot only the tone test until the user approves it")
    return errs, warns, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--lock", required=True)
    ap.add_argument("--brief")
    a = ap.parse_args()
    from lock import check
    lerrs, lk = check(a.lock, quiet=True)
    if lerrs:
        sys.exit("lock fails its integrity check: " + "; ".join(lerrs))
    brief = json.loads(Path(a.brief).read_text()) if a.brief else None
    errs, warns, info = lint(a.folder, lk, brief)
    for x in info:
        print("     ", x)
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    print(f"{'FAIL' if errs else 'PASS'}: {len(errs)} errors, {len(warns)} warnings (series {lk['manifest']['id']} v{lk['manifest']['version']})")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
