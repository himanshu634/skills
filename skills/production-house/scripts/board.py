#!/usr/bin/env python3
"""Render art-department sheets with the series' real kit, and build the art board.

Each sheet is a small scene module written exactly like a Motion scene
(kit.scene('id', {init(kit) {...}, render(t) {...}})), headed by a comment:

  /* @sheet
  title: The ticket office
  kind: set            (set | cast | look | frame)
  times: 2.0, 6.5      (moments to capture)
  dur: 8               (scene length the code assumes)
  palette: home        (a world from the spec; default = spec default)
  caption: Lamp on; the door opens at 6 s and spills cool light on the floor.
  check: true          (run the series frame checks on these captures)
  */

Usage:
  board.py LOCK.md SHEETS_DIR OUT_DIR [--auto] [--title T] [--note N]
  board.py --series series.js --spec spec.json SHEETS_DIR OUT_DIR ...   (before the first pack)

Writes OUT_DIR/png/*.png (full 1920x1080), OUT_DIR/checks.json and OUT_DIR/board.html
(self-contained, ready to publish as an artifact for the user's review and comments).
--auto adds the palette-and-type sheet and the cast lineup (every SERIES.cast member at
600, 200 and 80 px, to prove each reads by outline at small sizes).

The harness imitates Motion's scene API closely enough for sheets (stage, fx canvas,
h, css, dur, seg, eio, eo, lerp, rng); Motion itself remains the source of truth.
"""
import argparse
import base64
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;background:#000}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:system-ui,sans-serif}
#stage .ground{position:absolute;inset:0;background:var(--ground)}
#stage .words{position:absolute;margin:0;display:flex;flex-direction:column;gap:24px}
#stage .line{font-family:Georgia,serif;font-size:84px;line-height:1.05;color:var(--second)}
#stage .sub{font-size:34px;letter-spacing:.08em;color:var(--second)}
#fx{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:55;pointer-events:none}
</style></head><body><div id="stage"></div><canvas id="fx" width="1920" height="1080"></canvas>
<script>__SHARED__</script>
<script>
window.__make = function (pal, dur) {
  var fx = document.getElementById('fx'), old = document.getElementById('stage'), st = document.createElement('div'); st.id = 'stage';
  document.body.appendChild(fx); old.replaceWith(st);
  st.style.setProperty('--ground', pal[0]); st.style.setProperty('--main', pal[1]);
  st.style.setProperty('--second', pal[2]); st.style.setProperty('--accent', pal[3]);
  st.appendChild(fx);
  var c = fx.getContext('2d'); c.clearRect(0, 0, 1920, 1080);
  var kit = { stage: st, fx: c, W: 1920, H: 1080, dur: dur,
    seg: PH.seg, eio: PH.ease.inOut, eo: PH.ease.out, lerp: PH.lerp, rng: PH.rng, clamp01: PH.clamp01,
    h: function (s) { var t = document.createElement('template'); t.innerHTML = s.trim(); return t.content.firstElementChild; },
    css: function (s) { var e = document.createElement('style'); e.textContent = s; document.head.appendChild(e); },
    breathe: function (t, a) { return 1 + (a || 0.004) * Math.sin(t * 1.6); },
    scene: function (id, def) { window.__def = def; } };
  window.__kit = kit; return true;
};
window.__load = function (code) { new Function('kit', code)(window.__kit); var d = window.__def; d.init.call(d, window.__kit); return true; };
window.__render = function (t) { var c = window.__kit.fx; c.save(); c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,1920,1080); c.restore(); window.__def.render.call(window.__def, t); return true; };
</script></body></html>"""

AUTO_CAST = """/* @sheet
title: Cast lineup
kind: cast
times: 1.0
dur: 4
caption: Every cast member at 600 px, then 200 and 80 px: each must read by outline alone at the small sizes.
check: false
*/
kit.scene('cast-lineup', {
  init(kit) {
    kit.stage.append(kit.h('<div class="ground"></div>'));
    var svg = PH.svg(kit), ids = Object.keys(SERIES.cast), n = Math.max(1, ids.length), self = this;
    this.figs = [];
    ids.forEach(function (id, i) {
      var x = 1920 * (i + 0.5) / n;
      [[600, 0], [200, 1], [80, 2]].forEach(function (s) {
        var f = SERIES.cast[id](kit, svg, { x: s[1] === 0 ? x : x + (s[1] === 1 ? -90 : 90), y: s[1] === 0 ? 760 : 1030, h: s[0], facing: 1 });
        self.figs.push(f);
      });
      var lab = document.createElement('div'); lab.textContent = id;
      lab.style.cssText = 'position:absolute;top:780px;width:400px;text-align:center;font:600 30px system-ui,sans-serif;color:var(--second);left:' + (x - 200) + 'px';
      kit.stage.appendChild(lab);
    });
  },
  render(t) { this.figs.forEach(function (f) { if (f.pose) f.pose({}); }); }
});
"""

AUTO_PALETTE = """/* @sheet
title: Palettes and type
kind: look
times: 0.5
dur: 2
caption: Each world's four colors (ground, main, second, accent) and the series' typefaces.
check: false
*/
kit.scene('palettes', {
  init(kit) {
    var spec = __SPEC__, worlds = spec.palettes.worlds, names = Object.keys(worlds), y = 90;
    kit.stage.style.background = '#1b1b1b';
    names.forEach(function (w) {
      var row = document.createElement('div');
      row.style.cssText = 'position:absolute;left:120px;top:' + y + 'px;display:flex;gap:18px;align-items:center';
      row.innerHTML = '<div style="width:260px;font:600 34px system-ui,sans-serif;color:#eee">' + w + (w === spec.palettes.default ? ' (default)' : '') + '</div>' +
        worlds[w].map(function (c, i) { return '<div style="width:250px;height:150px;background:' + c + ';border:1px solid #555;display:flex;align-items:flex-end;padding:10px;box-sizing:border-box;font:22px monospace;color:' + (i === 0 ? '#ccc' : '#111') + '">' + ['ground','main','second','accent'][i] + ' ' + c + '</div>'; }).join('');
      kit.stage.appendChild(row); y += 200;
    });
    var f = spec.fonts || {}, t = document.createElement('div');
    t.style.cssText = 'position:absolute;left:120px;top:' + (y + 20) + 'px;color:#eee;font:28px system-ui,sans-serif;line-height:1.6';
    t.innerHTML = Object.keys(f).map(function (k) { var v = f[k]; return k + ': ' + (v.family || v) + (v.or ? ' (Motion fallback ' + v.or + ')' : ''); }).join('<br>') + '<br><span style="color:#999;font-size:22px">Typefaces are named here; Motion loads them in the film.</span>';
    kit.stage.appendChild(t);
  },
  render(t) {}
});
"""


def header(code):
    m = re.search(r"/\*\s*@sheet(.*?)\*/", code, re.S)
    if not m:
        return None
    h = {}
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            h[k.strip()] = re.sub(r"\s+\(.*\)$", "", v.strip())
    h["times"] = [float(x) for x in h.get("times", "1").split(",")]
    h["dur"] = float(h.get("dur", max(h["times"]) + 1))
    h["check"] = h.get("check", "false").lower() == "true"
    return h


def thumb(png, width=1280):
    im = Image.open(io.BytesIO(png)).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


BOARD_CSS = """
:root{--bg:#f6f4ef;--fg:#1d1c1a;--mut:#6a665e;--card:#fff;--line:#ddd8cc;--ok:#2f6b3a;--bad:#a1352b;color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#151514;--fg:#ecebe6;--mut:#a29e94;--card:#1f1f1d;--line:#34332f;--ok:#7cc48a;--bad:#e58b80;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#151514;--fg:#ecebe6;--mut:#a29e94;--card:#1f1f1d;--line:#34332f;--ok:#7cc48a;--bad:#e58b80;color-scheme:dark}
:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;margin:0 auto;padding:28px 18px 60px}
h1{font:600 30px/1.2 Georgia,"Times New Roman",serif;margin:0 0 6px}
.meta{color:var(--mut);margin:0 0 6px}.note{max-width:780px}
section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:22px 0}
h2{font:600 21px/1.3 Georgia,serif;margin:0 0 4px}.kind{font:600 12px system-ui;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.shots{display:grid;gap:12px;margin-top:12px}figure{margin:0}img{width:100%;max-width:100%;height:auto;display:block;border-radius:6px}
figcaption{color:var(--mut);font-size:14px;margin-top:4px}.ok{color:var(--ok)}.bad{color:var(--bad)}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("args", nargs="+")
    ap.add_argument("--series"); ap.add_argument("--spec"); ap.add_argument("--engine")
    ap.add_argument("--auto", action="store_true"); ap.add_argument("--title"); ap.add_argument("--note", default="")
    a = ap.parse_args()
    from lock import read, check, shared, ENGINE
    if a.series:
        sheets_dir, out = map(Path, a.args)
        spec = json.loads(Path(a.spec).read_text())
        eng = Path(a.engine).read_text() if a.engine else ENGINE.read_text()
        code_shared, version, status = eng + "\n" + Path(a.series).read_text(), spec.get("version", "?"), "draft (unpacked)"
    else:
        lockp, sheets_dir, out = a.args[0], Path(a.args[1]), Path(a.args[2])
        errs, p = check(lockp, quiet=True)
        if errs:
            sys.exit("lock fails its integrity check: " + "; ".join(errs))
        spec, code_shared, version, status = p["spec"], shared(p), p["manifest"]["version"], p["status"]
    from analyze_frames import analyze
    worlds = spec["palettes"]["worlds"]
    default = spec["palettes"].get("default") or next(iter(worlds))
    sheets = []
    if a.auto:
        sheets.append(("auto-palettes", AUTO_PALETTE.replace("__SPEC__", json.dumps(spec))))
        sheets.append(("auto-cast", AUTO_CAST))
    for f in sorted(sheets_dir.glob("*.js")):
        sheets.append((f.stem, f.read_text()))
    (out / "png").mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    results, sections = {}, []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1920, "height": 1080})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.set_content(PAGE.replace("__SHARED__", code_shared.replace("</script", "<\\/script")))
        for name, code in sheets:
            h = header(code)
            if not h:
                print(f"skip {name}: no @sheet header"); continue
            pal = worlds.get(h.get("palette", default), worlds[default])
            errors.clear()
            pg.evaluate("([p, d]) => __make(p, d)", [pal, h["dur"]])
            try:
                pg.evaluate("c => __load(c)", code)
            except Exception as e:
                errors.append(str(e).splitlines()[0])
            shots = []
            for t in h["times"]:
                if errors:
                    break
                try:
                    pg.evaluate("t => __render(t)", t)
                except Exception as e:
                    errors.append(str(e).splitlines()[0]); break
                png = pg.screenshot(clip={"x": 0, "y": 0, "width": 1920, "height": 1080})
                fn = out / "png" / f"{name}@{t:g}s.png"
                fn.write_bytes(png)
                r = analyze(Image.open(fn), spec.get("frames", {}) if h["check"] else {})
                results[fn.name] = r
                shots.append((t, png, r))
            if errors:
                print(f"ERROR {name}: {errors[0]}")
                results[name] = {"error": errors[0]}
            else:
                bad = [f"{s[0]:g}s: " + ", ".join(k for k, v in s[2]["checks"].items() if not v) for s in shots if not all(s[2]["checks"].values())]
                print(f"{'OK  ' if not bad else 'WARN'} {name}: {len(shots)} capture(s)" + (f"  failing {'; '.join(bad)}" if bad else ""))
            figs = "".join(
                f'<figure><img src="{thumb(png)}" alt="{html.escape(h.get("title", name))} at {t:g} s">'
                f'<figcaption>{t:g} s' + (
                    " · " + " ".join(f'<span class="{"ok" if v else "bad"}">{html.escape(k)} {"✓" if v else "✗"}</span>'
                                     for k, v in r["checks"].items() if not k.startswith("U1")) if h["check"] else "")
                + "</figcaption></figure>" for t, png, r in shots)
            err = f'<p class="bad">This sheet failed to render: {html.escape(errors[0])}</p>' if errors else ""
            sections.append(f'<section><div class="kind">{html.escape(h.get("kind", "sheet"))}</div><h2>{html.escape(h.get("title", name))}</h2>'
                            f'<p>{html.escape(h.get("caption", ""))}</p>{err}<div class="shots">{figs}</div></section>')
        br.close()
    title = a.title or f"Art board: {spec.get('title', spec.get('series'))}"
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{html.escape(title)}</title><style>{BOARD_CSS}</style></head><body><main><h1>{html.escape(title)}</h1>'
            f'<p class="meta">Series kit v{html.escape(version)} · {html.escape(status)} · rendered with the kit itself</p>'
            f'<p class="note">{html.escape(a.note)}</p>{"".join(sections)}</main></body></html>')
    (out / "board.html").write_text(page)
    (out / "checks.json").write_text(json.dumps(results, indent=1, default=bool))
    print(f"board: {out / 'board.html'} ({len(sections)} sheets)")


if __name__ == "__main__":
    main()
