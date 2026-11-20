#!/usr/bin/env python3
"""Measure frames or a film against universal checks and the series' own frame spec.

Usage:
  analyze_frames.py frame1.png frame2.png ... [--lock LOCK.md | --spec spec.json]
  analyze_frames.py film.mp4 [--samples 12] [--lock LOCK.md]
  analyze_frames.py FOLDER_OF_PNGS [--lock LOCK.md] [--json]

Universal (every series):
  U1 not empty      the frame has content (not a black or blank screen)
  U2 thumbnail      the first frame of a film is not black or empty (video input, or --first)
  U3 flash rate     no more than 3 flashes in any one second (video input only)
Series checks (only those the lock's spec "frames" section declares):
  dark_share        share of picture pixels below a luminance threshold, within [min, max]
  bright_share      share of pixels above a threshold, within [min, max] (for high-key looks)
  highlight         the brightest 0.3% of pixels reach a luminance
  light_offset      the lit area's centroid sits off centre (light comes from somewhere)
  texture_in_darks  fine texture present in dark areas (banding risk)
  matte             bars match the aspect (aspect 0 = no bars allowed)
Exit 1 if any check fails.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent


def load_frames_spec(lock=None, spec=None):
    if lock:
        sys.path.insert(0, str(HERE))
        from lock import read
        return read(lock)["spec"].get("frames", {})
    if spec:
        return json.loads(Path(spec).read_text()).get("frames", {})
    return {}


def luma(img):
    a = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def find_bars(L, vertical=False):
    if vertical:
        L = L.T
    n = L.shape[0]
    # matte bars are drawn as one flat color with no texture: near-black and uniform edge to edge
    flat = (L.mean(axis=1) < 0.05) & ((L.max(axis=1) - L.min(axis=1)) < 0.012)
    a = 0
    while a < n // 3 and flat[a]:
        a += 1
    b = 0
    while b < n // 3 and flat[n - 1 - b]:
        b += 1
    return a, b


def box_blur(L, r=3):
    k = 2 * r + 1
    c = np.pad(np.pad(L, r, mode="edge").cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def analyze(img, fs, first=False):
    L = luma(img)
    H, W = L.shape
    m = fs.get("matte") or {}
    asp = m.get("aspect", 0)
    top, bot = find_bars(L)
    lef, rig = find_bars(L, vertical=True) if asp and asp < W / H else (0, 0)
    pic = L[top:H - bot, lef:W - rig] if (H - bot > top and W - rig > lef) else L
    ph, pw = pic.shape
    res = {"size": f"{W}x{H}", "bars": [top, bot, lef, rig]}
    checks = {}
    empty = float((pic < 0.04).mean()) > 0.97 or float(pic.std()) < 0.01
    checks["U1 not empty"] = not empty
    if first:
        checks["U2 thumbnail"] = not empty and float(pic.mean()) > 0.03
    if "dark_share" in fs:
        c = fs["dark_share"]
        d = float((pic < c.get("threshold", 0.12)).mean())
        res["dark_share"] = round(d, 3)
        checks["dark_share"] = c.get("min", 0) <= d <= c.get("max", 1)
    if "bright_share" in fs:
        c = fs["bright_share"]
        b = float((pic > c.get("threshold", 0.6)).mean())
        res["bright_share"] = round(b, 3)
        checks["bright_share"] = c.get("min", 0) <= b <= c.get("max", 1)
    if "highlight" in fs:
        p = float(np.percentile(pic, 99.7))
        res["highlight"] = round(p, 3)
        checks["highlight"] = p >= fs["highlight"].get("min", 0.55)
    if "light_offset" in fs:
        hi = pic >= np.percentile(pic, 90)
        ys, xs = np.nonzero(hi)
        cx, cy = 0.5, 0.5
        if len(xs):
            w = pic[ys, xs]
            cx, cy = float((xs * w).sum() / w.sum()) / pw, float((ys * w).sum() / w.sum()) / ph
        off = float(np.hypot(cx - 0.5, cy - 0.5))
        res["light_centroid"], res["light_offset"] = [round(cx, 2), round(cy, 2)], round(off, 3)
        checks["light_offset"] = off >= fs["light_offset"].get("min", 0.08)
    if "texture_in_darks" in fs:
        c = fs["texture_in_darks"]
        thr = fs.get("dark_share", {}).get("threshold", 0.12)
        mask = pic < thr
        g = float((pic - box_blur(pic, 3))[mask].std()) if mask.sum() > 100 else 1.0
        res["texture_in_darks"] = round(g, 4)
        checks["texture_in_darks"] = g >= c.get("min", 0.004)
    if m:
        tol = m.get("tol_px", 6)
        if not asp or abs(asp - W / H) < 0.01:
            ok = min(top, bot) <= tol and min(lef, rig) <= tol  # a matte has bars on both edges
        elif asp > W / H:
            e = max(0, round((H - W / asp) / 2)); ok = abs(top - e) <= tol and abs(bot - e) <= tol
        else:
            e = max(0, round((W - H * asp) / 2)); ok = abs(lef - e) <= tol and abs(rig - e) <= tol
        checks["matte"] = ok
    res["checks"] = checks
    return res


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def frames_from_video(path, n):
    out, dur, files = Path(tempfile.mkdtemp()), probe(path), []
    for i in range(n):
        t = 0.0 if i == 0 else dur * (i + 0.5) / n
        f = out / f"t_{t:07.2f}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1", str(f)])
        if not f.exists():
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-ss", f"{max(0, t - 0.5):.3f}", "-frames:v", "1", str(f)])
        if f.exists():
            files.append(f)
    return files


def flash_rate(path, fps=24, delta=0.10):
    """Max flashes in any one-second window (a flash = a pair of opposing luminance swings >= delta)."""
    w, h = 160, 90
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={w}:{h}", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    n = len(raw) // (w * h)
    if n < 3:
        return 0.0, n
    mean = np.frombuffer(raw[:n * w * h], dtype=np.uint8).reshape(n, w * h).mean(axis=1) / 255.0
    turns, anchor, peak, direction = [], 0, 0, 0
    for i in range(1, n):
        if direction == 0:
            if abs(mean[i] - mean[anchor]) >= delta:
                direction = 1 if mean[i] > mean[anchor] else -1
                peak = i
            continue
        if (mean[i] - mean[peak]) * direction > 0:
            peak = i  # still moving the same way: extend the swing
        elif abs(mean[i] - mean[peak]) >= delta:
            turns.append(peak)  # a reversal of at least delta: the peak was a turning point
            direction, peak = -direction, i
    times = np.array(turns) / fps
    worst = max((int(((times >= t0) & (times < t0 + 1.0)).sum()) for t0 in times), default=0)
    return worst / 2.0, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--lock")
    ap.add_argument("--spec")
    ap.add_argument("--samples", type=int, default=12)
    ap.add_argument("--first", action="store_true", help="treat the first image as the film's first frame")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    fs = load_frames_spec(a.lock, a.spec)
    files, videos = [], []
    for inp in a.inputs:
        p = Path(inp)
        if p.is_dir():
            files += sorted(x for x in p.iterdir() if x.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))
        elif p.suffix.lower() in (".mp4", ".mov", ".webm", ".mkv"):
            videos.append(p)
            files += frames_from_video(p, a.samples)
        else:
            files.append(p)
    results, failed = {}, 0
    for i, f in enumerate(files):
        r = analyze(Image.open(f), fs, first=(i == 0 and (a.first or bool(videos))))
        results[str(f)] = r
        failed += not all(r["checks"].values())
    film = {}
    for v in videos:
        fl, n = flash_rate(v)
        film[str(v)] = {"max_flashes_per_s": fl, "frames_scanned": n, "U3 flash rate": fl <= 3}
        failed += fl > 3
    if a.json:
        print(json.dumps({"frames": results, "films": film, "spec": fs}, indent=1, default=bool))
        sys.exit(1 if failed else 0)
    if not fs:
        print("No series frame spec given (--lock or --spec): universal checks only.")
    for f, r in results.items():
        bad = [k for k, v in r["checks"].items() if not v]
        vals = "  ".join(f"{k} {r[k]}" for k in ("dark_share", "bright_share", "highlight", "light_offset", "texture_in_darks") if k in r)
        print(f"{Path(f).name}: {vals}  bars {r['bars']}  {'OK' if not bad else 'FAIL ' + ', '.join(bad)}")
    for v, r in film.items():
        print(f"{Path(v).name}: max {r['max_flashes_per_s']:g} flashes/s over {r['frames_scanned']} frames  "
              f"{'OK' if r['U3 flash rate'] else 'FAIL U3 flash rate'}")
    print()
    for n in sorted({k for r in results.values() for k in r["checks"]}):
        have = [r for r in results.values() if n in r["checks"]]
        print(f"{n}: {sum(r['checks'][n] for r in have)}/{len(have)} frames pass")
    ok = sum(all(r["checks"].values()) for r in results.values())
    print(f"{'PASS' if not failed else 'FAIL'}: {ok}/{len(results)} frames meet the checks")
    print("Note: title cards, end cards and deliberate blackouts may fail series checks by design; judge them in context.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
