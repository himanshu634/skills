#!/usr/bin/env python3
"""Validate a shot brief against Motion's limits and the series lock, and emit what Motion needs.

Usage:
  brief.py validate brief.json --lock LOCK.md   errors exit 1; warnings are printed
  brief.py scenes   brief.json --lock LOCK.md   Motion's modules/scenes.json content
  brief.py basecss  brief.json --lock LOCK.md   the first modules/base.css
  brief.py settle   brief.json --lock LOCK.md   the line that settles Motion's three questions
"""
import argparse
import colorsys
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
MOTION = json.loads((HERE / "motion.json").read_text())
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
ID = re.compile(r"^[a-z][a-z0-9-]{0,31}$")


def classify(hexcol):
    r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if l < 0.16:
        return "black"
    if l > 0.8:
        return "white"
    if s > 0.35 and (h < 0.06 or h > 0.94) and 0.2 < l < 0.75:
        return "red"
    return "other"


def only_brw(p):
    return all(classify(c) in ("black", "red", "white") for c in p)


def palette_order(b, spec):
    worlds = spec["palettes"]["worlds"]
    order = list(b.get("palette_order") or [])
    used = [s.get("palette") for s in b.get("scenes", []) if s.get("palette")]
    for w in [spec["palettes"].get("default")] + used:
        if w and w not in order:
            order.append(w)
    return [w for w in order if w in worlds]


def validate(b, lk):
    errs, warns = [], []
    spec, man, status = lk["spec"], lk["manifest"], lk["status"]
    vocab, con = man["vocab"], spec.get("scene_contract", {})
    for k in ("title", "about", "scenes", "lock"):
        if k not in b:
            errs.append(f"missing top-level '{k}'")
    if errs:
        return errs, warns
    if b["lock"].get("series") != man["id"]:
        errs.append(f"brief is for series '{b['lock'].get('series')}', lock is '{man['id']}'")
    if b["lock"].get("version") != man["version"]:
        errs.append(f"brief written against lock v{b['lock'].get('version')}, lock is v{man['version']}: re-check the brief")
    kind = b.get("kind", "film")
    if kind == "film" and status != "approved":
        errs.append("the lock is still a draft: shoot the tone test and freeze the lock (gate 3) before the full film")
    scenes = b["scenes"]
    if not scenes:
        errs.append("no scenes")
    if len(scenes) > MOTION["max_scenes"]:
        errs.append(f"{len(scenes)} scenes; Motion allows at most {MOTION['max_scenes']}")
    total = sum(float(s.get("dur", 0)) for s in scenes)
    if total > MOTION["max_total_s"]:
        errs.append(f"total {total:.1f}s exceeds Motion's {MOTION['max_total_s']}s cap; split into several films")
    if kind == "tone-test" and not (4 <= total <= 15):
        warns.append(f"tone test runs {total:g}s; 6-10 s of the riskiest scene is enough")
    fps = spec.get("stage", {}).get("fps", 24)
    if fps not in MOTION["fps_allowed"]:
        errs.append(f"lock fps {fps} not in Motion's {MOTION['fps_allowed']}")
    worlds = spec["palettes"]["worlds"]
    for w, p in worlds.items():
        if len(p) != 4 or not all(HEX.match(c) for c in p):
            errs.append(f"palette '{w}' must be four #rrggbb colors (ground, main, second, accent)")
        elif only_brw(p) and not con.get("allow_black_red_white"):
            errs.append(f"palette '{w}' reads as only black/red/white-cream, which Motion avoids unless the user asked")
    for slot, v in (spec.get("fonts") or {}).items():
        if not (isinstance(v, dict) and v.get("family") and v.get("or") in MOTION["shipped_fonts"]) and v not in MOTION["shipped_fonts"]:
            errs.append(f"font '{slot}' needs a family and an 'or' from Motion's shipped faces")
    ids, local_sets, lens_count = set(), {}, {}
    cap = con.get("max_words_per_scene", 12)
    for n, s in enumerate(scenes, 1):
        sid = s.get("id", "")
        tag = f"scene {n} ({sid or '?'})"
        if not ID.match(sid):
            errs.append(f"{tag}: id must be lowercase letters, digits, '-', letter first, 32 max")
        if sid in ids:
            errs.append(f"{tag}: duplicate id")
        ids.add(sid)
        name = s.get("name", "")
        if not name or len(name) > 48:
            errs.append(f"{tag}: name required, 48 characters max")
        dur = float(s.get("dur", 0))
        if dur < MOTION["min_scene_s"]:
            errs.append(f"{tag}: dur {dur}s is under {MOTION['min_scene_s']}s")
        if dur > 30:
            warns.append(f"{tag}: {dur}s is long for one Motion scene (one subject, one action)")
        if not s.get("desc"):
            errs.append(f"{tag}: desc (one plain sentence) required")
        led = s.get("ledger") or {}
        if not led.get("start") or not led.get("end"):
            errs.append(f"{tag}: ledger needs start and end")
        elif led["start"].strip().lower() == led["end"].strip().lower():
            errs.append(f"{tag}: the ledger doesn't change, so the scene doesn't turn. Cut or merge it")
        if not s.get("screenplay"):
            warns.append(f"{tag}: no 'screenplay' reference to the approved screenplay scene")
        st = s.get("set")
        if isinstance(st, str):
            if st not in vocab["sets"]:
                errs.append(f"{tag}: set '{st}' is not in the lock ({vocab['sets'] or 'none designed'}). Design it in the art department first")
        elif isinstance(st, dict) and st.get("local"):
            local_sets.setdefault(st["local"].strip().lower(), []).append(sid)
        else:
            errs.append(f"{tag}: 'set' must name a lock set, or be {{\"local\": \"one-line description\"}} for a one-off place")
        for c in s.get("cast") or []:
            if c.get("id") not in vocab["cast"]:
                errs.append(f"{tag}: cast '{c.get('id')}' is not in the lock ({vocab['cast'] or 'none designed'}). Design the character first")
        for li in s.get("light") or []:
            if li.get("recipe") not in vocab["light"]:
                errs.append(f"{tag}: light recipe '{li.get('recipe')}' is not in the lock {vocab['light']}")
        mode = (s.get("lens") or {}).get("mode")
        if mode not in vocab["lens"]:
            errs.append(f"{tag}: lens mode '{mode}' is not in the lock {vocab['lens']}")
        lens_count[mode] = lens_count.get(mode, 0) + 1
        for lv in s.get("living") or []:
            if lv not in vocab["living"]:
                errs.append(f"{tag}: living element '{lv}' is not in the lock {vocab['living']}")
        if s.get("palette") and s["palette"] not in worlds:
            errs.append(f"{tag}: palette '{s['palette']}' is not a world in the lock {list(worlds)}")
        times = [bt.get("t", 0) for bt in s.get("beats") or []]
        if times != sorted(times):
            errs.append(f"{tag}: beats out of order")
        if any(t0 > dur for t0 in times):
            errs.append(f"{tag}: a beat falls after the scene ends")
        words = sum(len(str(x).split()) for x in (s.get("text") or []))
        if words > cap and n not in (1, len(scenes)):
            warns.append(f"{tag}: {words} words on screen (series cap {cap})")
        if s.get("vo") and b.get("voice_model") == "silent":
            warns.append(f"{tag}: VO lines in a silent-model series go to the post sheet only")
    for desc, where in local_sets.items():
        if len(where) > 1:
            warns.append(f"local set '{desc}' is used in {len(where)} scenes ({', '.join(where)}): a recurring place belongs in the lock")
    for bud in con.get("budgets", []):
        mode = bud.get("lens_mode")
        if not mode:
            continue
        n = lens_count.get(mode, 0)
        cap = bud["per_film"] if "per_film" in bud else max(bud.get("min", 0), round(total / 60 * bud.get("per_60s", 1)))
        if n > cap:
            errs.append(f"lens '{mode}' used {n}x; the series budget is {cap} ({bud.get('why', '')})")
    return errs, warns


def scenes_json(b, lk):
    spec = lk["spec"]
    order = palette_order(b, spec)
    pals = [spec["palettes"]["worlds"][w] for w in order]
    look = f"{spec['look']['name']}: {spec['look']['line']} | Series lock {lk['manifest']['id']} v{lk['manifest']['version']}"
    if b.get("user_words"):
        look += f" | User's words: {b['user_words']}"
    out = {"v": 1, "stage": "rough", "look": look, "palettes": pals, "theirs": 0, "width": 1920, "height": 1080,
           "fps": spec.get("stage", {}).get("fps", 24), "background": pals[0][0]}
    if spec.get("fonts"):
        out["fonts"] = spec["fonts"]
    out["scenes"] = [{"id": s["id"], "name": s["name"], "dur": s["dur"], "desc": s["desc"]} for s in b["scenes"]]
    return out


def base_css(b, lk):
    spec = lk["spec"]
    g, m, s2, a = spec["palettes"]["worlds"][palette_order(b, spec)[0]]
    disp = "var(--display, var(--serif, Georgia, serif))"
    return "\n".join([
        f"#stage {{ --ground:{g}; --main:{m}; --second:{s2}; --accent:{a}; color:var(--second); font-family:var(--sans, system-ui, sans-serif) }}",
        ".ground { position:absolute; inset:0; background:var(--ground) }",
        ".words { position:absolute; margin:0; display:flex; flex-direction:column; gap:24px } .words > * { margin:0 }",
        f".line {{ font-family:{disp}; font-size:84px; line-height:1.05; font-weight:400; letter-spacing:.02em }}",
        ".sub { font-size:34px; letter-spacing:.08em }",
    ])


def settle(b, lk):
    spec = lk["spec"]
    p = spec["palettes"]["worlds"][palette_order(b, spec)[0]]
    total = sum(float(s["dur"]) for s in b["scenes"])
    return f"Animation details — Style: {spec['look']['name']}, {spec['look']['line']} · Colors: {' '.join(p)} · Length: {total:g} s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["validate", "scenes", "basecss", "settle"])
    ap.add_argument("brief")
    ap.add_argument("--lock", required=True)
    a = ap.parse_args()
    from lock import check
    lerrs, lk = check(a.lock, quiet=True)
    if lerrs:
        sys.exit("lock fails its integrity check: " + "; ".join(lerrs))
    b = json.loads(Path(a.brief).read_text())
    errs, warns = validate(b, lk)
    if a.cmd == "validate":
        for w in warns:
            print("WARN ", w)
        for e in errs:
            print("ERROR", e)
        total = sum(float(s.get("dur", 0)) for s in b.get("scenes", []))
        print(f"{'FAIL' if errs else 'PASS'}: {len(b.get('scenes', []))} scenes, {total:g} s, {len(errs)} errors, {len(warns)} warnings")
        sys.exit(1 if errs else 0)
    if errs:
        sys.exit("Brief has errors; run validate first.")
    if a.cmd == "scenes":
        print(json.dumps(scenes_json(b, lk), ensure_ascii=False, indent=1))
    elif a.cmd == "basecss":
        print(base_css(b, lk))
    else:
        print(settle(b, lk))


if __name__ == "__main__":
    main()
