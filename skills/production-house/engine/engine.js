/* PH engine: the look-neutral core of every Production House series kit.
   It has no visual opinion: no palette, no light recipe, no lens grammar, no character.
   A series layer (written per series in the art department) composes these primitives
   into that series' own look, and the pair is frozen together in the series lock.
   Rules: every helper takes the SCENE's kit first; everything is a pure function of t
   (no timers, no Math.random, no CSS transitions). */
(function () {
  var E = { version: '2.0' };
  var PIC = new WeakMap();

  /* ---------- time ---------- */
  function clamp01(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function seg(t, a, b) { return b === a ? (t >= b ? 1 : 0) : clamp01((t - a) / (b - a)); }
  function lerp(a, b, p) { return a + (b - a) * p; }
  function mod1(x) { return ((x % 1) + 1) % 1; }
  var ease = {
    linear: function (x) { return x; },
    inOut: function (x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; },
    out: function (x) { return 1 - Math.pow(1 - x, 3); },
    in: function (x) { return x * x * x; },
    sine: function (x) { return -(Math.cos(Math.PI * x) - 1) / 2; },
    back: function (x) { var c = 1.70158, d = c + 1; return 1 + d * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }
  };
  function rng(seed) {
    var s = (seed * 2654435761) >>> 0 || 1;
    return function () { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
  }
  function noise(seed) {
    var r = rng(seed), v = []; for (var i = 0; i < 256; i++) v.push(r() * 2 - 1);
    return function (x) {
      var i0 = Math.floor(x), f = x - i0, a = v[((i0 % 256) + 256) % 256], b = v[(((i0 + 1) % 256) + 256) % 256];
      var u = f * f * (3 - 2 * f); return a + (b - a) * u;
    };
  }
  /* Keyframes eased between keys: E.key(t, [[0, 0], [2, 30], [5, 30]]). Values may be arrays.
     Two equal keys make a hold. ease: a function or a name from E.ease. */
  function key(t, keys, ez) {
    ez = typeof ez === 'string' ? ease[ez] : (ez || ease.inOut);
    if (t <= keys[0][0]) return keys[0][1];
    var last = keys[keys.length - 1]; if (t >= last[0]) return last[1];
    for (var i = 0; i < keys.length - 1; i++) {
      var a = keys[i], b = keys[i + 1];
      if (t >= a[0] && t <= b[0]) {
        var p = ez(seg(t, a[0], b[0]));
        if (Array.isArray(a[1])) return a[1].map(function (v, j) { return lerp(v, b[1][j], p); });
        return lerp(a[1], b[1], p);
      }
    }
    return last[1];
  }
  /* Opacity in over [a,b], out over [c,d]. */
  function fade(t, a, b, c, d) {
    var v = ease.inOut(seg(t, a, b));
    if (c !== undefined) v *= 1 - ease.inOut(seg(t, c, d));
    return v;
  }
  function osc(t, period, amp, phase) { return (amp || 1) * Math.sin(2 * Math.PI * (t / period + (phase || 0))); }
  E.clamp01 = clamp01; E.seg = seg; E.lerp = lerp; E.mod1 = mod1; E.ease = ease; E.rng = rng;
  E.noise = noise; E.key = key; E.fade = fade; E.osc = osc;

  /* ---------- stage and DOM ---------- */
  function W(kit) { return kit.W || 1920; }
  function H(kit) { return kit.H || 1080; }
  function div(kit, parent, css, before) {
    var d = document.createElement('div');
    d.style.position = 'absolute'; d.style.pointerEvents = 'none';
    for (var k in css) d.style[k] = css[k];
    parent = parent || kit.stage;
    if (before && before.parentNode === parent) parent.insertBefore(d, before); else parent.appendChild(d);
    return d;
  }
  /* A full-stage layer (for sets, light, effects). o: z, before, css. */
  function layer(kit, parent, o) {
    o = o || {};
    var css = { left: '0px', top: '0px', width: W(kit) + 'px', height: H(kit) + 'px' };
    if (o.z !== undefined) css.zIndex = String(o.z);
    if (o.clip) css.overflow = 'hidden';
    for (var k in (o.css || {})) css[k] = o.css[k];
    return div(kit, parent, css, o.before);
  }
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in (attrs || {})) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e); return e;
  }
  /* A full-stage SVG in stage pixels. */
  function svg(kit, parent, o) {
    o = o || {};
    var s = el('svg', { viewBox: '0 0 ' + W(kit) + ' ' + H(kit) });
    s.style.position = 'absolute'; s.style.left = '0px'; s.style.top = '0px';
    s.style.width = W(kit) + 'px'; s.style.height = H(kit) + 'px'; s.style.overflow = 'visible';
    if (o.z !== undefined) s.style.zIndex = String(o.z);
    parent = parent || kit.stage;
    if (o.before && o.before.parentNode === parent) parent.insertBefore(s, o.before); else parent.appendChild(s);
    return s;
  }
  /* Colour helpers that keep the palette in the stage's CSS variables. */
  function mix(a, pct, b) { return 'color-mix(in srgb, ' + a + ' ' + pct + '%, ' + (b || 'transparent') + ')'; }
  E.W = W; E.H = H; E.div = div; E.layer = layer; E.el = el; E.svg = svg; E.mix = mix;

  /* ---------- picture area and matte ---------- */
  function picture(kit) { return PIC.get(kit.stage) || { x: 0, y: 0, w: W(kit), h: H(kit) }; }
  function setPicture(kit, r) { PIC.set(kit.stage, r); return r; }
  function clip(kit, ctx) { var p = picture(kit); ctx.beginPath(); ctx.rect(p.x, p.y, p.w, p.h); ctx.clip(); }
  /* Bars that matte the 16:9 stage to an aspect (horizontal bars if wider, vertical if narrower).
     aspect 0 or 16/9 draws nothing. Call last in init so it sits above the picture. */
  function matte(kit, o) {
    o = o || {};
    var a = o.aspect || 0, w = W(kit), h = H(kit), z = String(o.z || 60), bg = o.color || 'rgb(0,0,0)';
    if (!a || Math.abs(a - w / h) < 0.01) return { bars: [], picture: setPicture(kit, { x: 0, y: 0, w: w, h: h }) };
    var bars = [];
    if (a > w / h) {
      var b = Math.round((h - w / a) / 2);
      bars.push(div(kit, kit.stage, { left: '0px', top: '0px', width: w + 'px', height: b + 'px', background: bg, zIndex: z }));
      bars.push(div(kit, kit.stage, { left: '0px', top: (h - b) + 'px', width: w + 'px', height: b + 'px', background: bg, zIndex: z }));
      return { bars: bars, picture: setPicture(kit, { x: 0, y: b, w: w, h: h - 2 * b }) };
    }
    var s = Math.round((w - h * a) / 2);
    bars.push(div(kit, kit.stage, { left: '0px', top: '0px', width: s + 'px', height: h + 'px', background: bg, zIndex: z }));
    bars.push(div(kit, kit.stage, { left: (w - s) + 'px', top: '0px', width: s + 'px', height: h + 'px', background: bg, zIndex: z }));
    return { bars: bars, picture: setPicture(kit, { x: s, y: 0, w: w - 2 * s, h: h }) };
  }
  E.picture = picture; E.setPicture = setPicture; E.clip = clip; E.matte = matte;

  /* ---------- the shared canvas ---------- */
  function ctx(kit) { return kit.fx && kit.fx.canvas ? kit.fx : (kit.fx && kit.fx.getContext ? kit.fx.getContext('2d') : null); }
  var TILES = {};
  function tiles(mode, size) {
    var id = mode + size; if (TILES[id]) return TILES[id];
    var out = [];
    for (var k = 0; k < 4; k++) {
      var c = document.createElement('canvas'); c.width = c.height = size;
      var g = c.getContext('2d'), im = g.createImageData(size, size), r = rng(101 + k), waves = [];
      if (mode === 'soft') for (var q = 0; q < 10; q++) waves.push([Math.floor(r() * 7) - 3, Math.floor(r() * 7) - 3, r() * 6.283, 0.5 + r()]);
      for (var y = 0; y < size; y++) for (var x = 0; x < size; x++) {
        var i = (y * size + x) * 4, v = r();
        if (mode === 'soft') { /* seamless: integer frequencies across the tile */
          var sum = 0, tot = 0;
          for (var w = 0; w < waves.length; w++) { var wv = waves[w]; sum += wv[3] * Math.sin(6.2832 * (wv[0] * x + wv[1] * y) / size + wv[2]); tot += wv[3]; }
          v = clamp01(0.5 + 0.5 * sum / tot + 0.12 * (v - 0.5));
        }
        var on = v > 0.5 ? 255 : 0;
        im.data[i] = im.data[i + 1] = im.data[i + 2] = on; im.data[i + 3] = Math.round(Math.abs(v - 0.5) * 2 * 255);
      }
      g.putImageData(im, 0, 0); out.push(c);
    }
    TILES[id] = out; return out;
  }
  /* Surface texture over the picture. o: amount (alpha), rate (changes per second; 0 = static),
     mode ('grain' fine noise | 'soft' blotchy, paper-like), size (tile px), blend (canvas composite op). */
  function texture(kit, t, o) {
    o = o || {};
    var c = ctx(kit); if (!c) return;
    var size = o.size || (o.mode === 'soft' ? 256 : 160), rate = o.rate === undefined ? 24 : o.rate;
    var f = rate ? Math.floor(t * rate) : 0, r = rng(7919 + f), tl = tiles(o.mode || 'grain', size)[f % 4];
    c.save(); clip(kit, c);
    c.globalAlpha = o.amount === undefined ? 0.06 : o.amount;
    if (o.blend) c.globalCompositeOperation = o.blend;
    c.fillStyle = c.createPattern(tl, 'repeat');
    c.translate(Math.floor(r() * size), Math.floor(r() * size));
    c.fillRect(-size, -size, W(kit) + 2 * size, H(kit) + 2 * size);
    c.restore();
  }
  /* Canvas particles. o: n, seed, init(r, i) -> state, draw(ctx, state, t, i). Clipped to the picture. */
  function particles(kit, o) {
    var r = rng(o.seed || 5), st = [];
    for (var i = 0; i < (o.n || 30); i++) st.push(o.init(r, i));
    return {
      render: function (t) {
        var c = ctx(kit); if (!c) return;
        c.save(); clip(kit, c);
        for (var i = 0; i < st.length; i++) { c.save(); o.draw(c, st[i], t, i); c.restore(); }
        c.restore();
      }
    };
  }
  /* DOM sprites. o: n, css(i) -> style object, place(i, t) -> {x, y, s, sx, sy, r, o}. */
  function sprites(kit, parent, o) {
    var bits = [];
    for (var i = 0; i < o.n; i++) bits.push(div(kit, parent, Object.assign({ left: '0px', top: '0px' }, o.css(i)), o.before));
    return {
      els: bits,
      render: function (t) {
        for (var i = 0; i < bits.length; i++) {
          var p = o.place(i, t), sx = p.sx === undefined ? (p.s || 1) : p.sx, sy = p.sy === undefined ? (p.s || 1) : p.sy;
          bits[i].style.transform = 'translate(' + p.x + 'px,' + p.y + 'px) rotate(' + (p.r || 0) + 'deg) scale(' + sx + ',' + sy + ')';
          bits[i].style.opacity = String(p.o === undefined ? 1 : p.o);
        }
      }
    };
  }
  E.ctx = ctx; E.texture = texture; E.particles = particles; E.sprites = sprites;

  /* ---------- light primitives (layers a series composes into its own recipes) ----------
     Positions are fractions of the stage. Every primitive takes o.parent, o.before, o.z,
     and o.background to override its default gradient entirely. */
  function full(kit, o, css) {
    var c = { left: '0px', top: '0px', width: W(kit) + 'px', height: H(kit) + 'px' };
    if (!o.before) c.zIndex = String(o.z || 20);
    for (var k in css) c[k] = css[k];
    return div(kit, o.parent || kit.stage, c, o.before);
  }
  /* Darkness with a soft hole: shape 'radial' (x, y, rx, ry, inner 0..1) or 'linear' (angle, from %). */
  function shade(kit, o) {
    var dark = o.dark === undefined ? 0.85 : o.dark, sh = 'rgba(0,0,0,' + dark + ')', bg;
    if (o.shape === 'linear') bg = 'linear-gradient(' + (o.angle || 180) + 'deg, transparent ' + (o.from || 35) + '%, ' + sh + ')';
    else bg = 'radial-gradient(' + (o.rx || 0.35) * W(kit) + 'px ' + (o.ry || 0.3) * W(kit) + 'px at ' + (o.x === undefined ? 50 : o.x * 100) + '% ' + (o.y === undefined ? 50 : o.y * 100) + '%, transparent 0%, transparent ' + ((o.inner || 0.2) * 100) + '%, ' + sh + ' 100%)';
    return full(kit, o, { background: o.background || bg });
  }
  /* A pool of light: radial glow of color with stops [[pct, alpha%], ...]. */
  function pool(kit, o) {
    var stops = (o.stops || [[0, 100], [9, 62], [26, 38], [100, 0]]).map(function (s) { return mix(o.color, s[1]) + ' ' + s[0] + '%'; }).join(', ');
    var bg = 'radial-gradient(' + (o.rx || 0.3) * W(kit) + 'px ' + (o.ry || 0.25) * W(kit) + 'px at ' + o.x * 100 + '% ' + o.y * 100 + '%, ' + stops + ')';
    return full(kit, o, { background: o.background || bg });
  }
  /* A beam: polygon (fractions) filled with a gradient along angle, from alpha a0% to a1%. */
  function beam(kit, o) {
    var poly = o.poly.map(function (p) { return p[0] * 100 + '% ' + p[1] * 100 + '%'; }).join(', ');
    var bg = 'linear-gradient(' + (o.angle === undefined ? 180 : o.angle) + 'deg, ' + mix(o.color, o.a0 === undefined ? 70 : o.a0) + ', ' + mix(o.color, o.a1 === undefined ? 15 : o.a1) + ')';
    return full(kit, o, { clipPath: 'polygon(' + poly + ')', background: o.background || bg, filter: o.blur ? 'blur(' + o.blur + 'px)' : '' });
  }
  /* A directional wash across the whole frame. */
  function wash(kit, o) {
    var bg = 'linear-gradient(' + (o.angle === undefined ? 110 : o.angle) + 'deg, ' + mix(o.color, o.a0 === undefined ? 34 : o.a0) + ', transparent ' + (o.reach || 60) + '%)';
    return full(kit, o, { background: o.background || bg });
  }
  /* A visible source (bulb, flame, moon): a small glowing disc. */
  function glow(kit, o) {
    var s = o.size || 40;
    return div(kit, o.parent || kit.stage, {
      left: o.x * W(kit) - s / 2 + 'px', top: o.y * H(kit) - s / 2 + 'px', width: s + 'px', height: (o.h || s) + 'px',
      borderRadius: '50%', zIndex: String(o.z || 20),
      background: o.background || 'radial-gradient(closest-side, ' + (o.core || 'rgb(255,250,236)') + ', ' + o.color + ' 30%, ' + mix(o.color, 40) + ' 60%, transparent)'
    }, o.before);
  }
  /* A controller that drives composed light layers over time.
     parts: [{el, k, flick}]: k scales that layer's opacity (default 1); flick is how much of the
     flicker reaches it (default 1; 0 = steady, 0.15 = a bulb that barely wavers).
     keys: [[t, level], ...] to switch on/off; flicker: 0..0.08 slow noise; seed.
     blackout: {dark} adds a layer that darkens the frame as the level falls (a light going out). */
  function light(kit, o) {
    var parts = o.parts || [], fl = o.flicker || 0, nz = noise(o.seed || 11), keys = o.keys, bo = null;
    if (o.blackout) bo = full(kit, o, { background: 'rgba(0,0,0,' + Math.min(0.94, o.blackout.dark) + ')', opacity: '0' });
    function level(t) { return keys ? key(t, keys) : 1; }
    return {
      parts: parts, level: level,
      render: function (t) {
        var lv = level(t), f = 1 + fl * (nz(t * 1.7) * 0.7 + nz(t * 4.3 + 40) * 0.3);
        parts.forEach(function (p) { var fk = p.flick === undefined ? 1 : p.flick; p.el.style.opacity = String(clamp01(lv * (1 + fk * (f - 1)) * (p.k === undefined ? 1 : p.k))); });
        if (bo) bo.style.opacity = String(1 - lv);
      }
    };
  }
  E.shade = shade; E.pool = pool; E.beam = beam; E.wash = wash; E.glow = glow; E.light = light;

  /* ---------- camera ----------
     layers: one element or [[el, depth], ...] (1 = main plane, <1 far, >1 near) for parallax.
     motion(t) -> {s, x, y, r}. o: fx, fy (focus, fractions). A series defines its lens grammar
     as named motions built from the helpers below. */
  function camera(kit, layers, motion, o) {
    o = o || {};
    if (!Array.isArray(layers)) layers = [[layers, 1]];
    var fx = (o.fx === undefined ? 0.5 : o.fx) * W(kit), fy = (o.fy === undefined ? 0.5 : o.fy) * H(kit);
    layers.forEach(function (l) { l[0].style.transformOrigin = fx + 'px ' + fy + 'px'; });
    var api = { state: { s: 1, x: 0, y: 0, r: 0 } };
    api.apply = function (t) {
      var m = motion(t) || {}, s = m.s === undefined ? 1 : m.s, x = m.x || 0, y = m.y || 0, r = m.r || 0;
      api.state = { s: s, x: x, y: y, r: r };
      layers.forEach(function (l) {
        var d = l[1];
        l[0].style.transform = 'translate(' + x * d + 'px,' + y * d + 'px) rotate(' + r + 'deg) scale(' + (1 + (s - 1) * d) + ')';
      });
      return api.state;
    };
    return api;
  }
  /* Motion building blocks. */
  function shake(seed) {
    var a = noise(seed * 7 + 1), b = noise(seed * 7 + 2), c = noise(seed * 7 + 3);
    return function (t, amp, roll, speed) { var k = speed || 1; return { x: amp * a(t * 0.6 * k), y: amp * 0.6 * b(t * 0.5 * k), r: (roll || 0) * c(t * 0.4 * k) }; };
  }
  /* Scale needed so a frame rotated by deg still covers the stage. */
  function cover(kit, deg) { var th = Math.abs(deg) * Math.PI / 180; return Math.cos(th) + (W(kit) / H(kit)) * Math.sin(th); }
  E.camera = camera; E.shake = shake; E.cover = cover;

  /* ---------- rigs ----------
     A jointed, drawn character of any design. parts: [{id, parent, pivot: [x, y], draw}],
     in the rig's own units (feet at 0,0; up is negative y). parent is another part's id or omitted
     for the root. draw is an SVG path string, or a function (g, E) that draws into the part's group.
     o: x, y (stage px), scale (px per unit), facing (1 | -1), fill, stroke, filter.
     pose({x, y, lean, opacity, joints: {id: angle | {r, sx, sy, dx, dy}}}). */
  function rig(kit, host, o) {
    var root = el('g', {}, host), groups = {};
    if (o.fill) root.style.fill = o.fill;
    if (o.stroke) { root.style.stroke = o.stroke; root.style.strokeWidth = String(o.strokeWidth || 1); }
    if (o.filter) root.style.filter = o.filter;
    (o.parts || []).forEach(function (p) {
      var par = p.parent ? groups[p.parent].g : root, g = el('g', {}, par);
      if (typeof p.draw === 'string') el('path', { d: p.draw }, g); else if (p.draw) p.draw(g, E);
      groups[p.id] = { g: g, pivot: p.pivot || [0, 0] };
    });
    var api = { root: root, part: function (id) { return groups[id] && groups[id].g; } };
    api.pose = function (p) {
      p = p || {};
      var x = p.x === undefined ? o.x || 0 : p.x, y = p.y === undefined ? o.y || 0 : p.y, sc = o.scale || 3, f = o.facing || 1;
      root.setAttribute('transform', 'translate(' + x + ' ' + y + ') scale(' + sc * f + ' ' + sc + ') rotate(' + (p.lean || 0) + ')');
      if (p.opacity !== undefined) root.style.opacity = String(p.opacity);
      var j = p.joints || {};
      for (var id in groups) {
        var v = j[id], q = groups[id].pivot, tr = '';
        if (v === undefined) { groups[id].g.removeAttribute('transform'); continue; }
        if (typeof v === 'number') v = { r: v };
        if (v.dx || v.dy) tr += 'translate(' + (v.dx || 0) + ' ' + (v.dy || 0) + ') ';
        if (v.r) tr += 'rotate(' + v.r + ' ' + q[0] + ' ' + q[1] + ') ';
        if (v.sx !== undefined || v.sy !== undefined) tr += 'translate(' + q[0] + ' ' + q[1] + ') scale(' + (v.sx === undefined ? 1 : v.sx) + ' ' + (v.sy === undefined ? 1 : v.sy) + ') translate(' + (-q[0]) + ' ' + (-q[1]) + ')';
        groups[id].g.setAttribute('transform', tr.trim());
      }
    };
    api.pose({});
    return api;
  }
  /* A gait over [a, b] from x0 to x1: {x, phase (0..1 per step pair), moving, swing (-1..1), lift (0..1)}. */
  function gait(t, a, b, x0, x1, steps, ez) {
    var p = seg(t, a, b), q = ez ? (typeof ez === 'string' ? ease[ez] : ez)(p) : p, ph = p * (steps || 6) / 2;
    var moving = t > a && t < b, sw = Math.sin(ph * 2 * Math.PI);
    return { x: lerp(x0, x1, q), phase: mod1(ph), moving: moving, swing: moving ? sw : 0, lift: moving ? Math.abs(sw) : 0 };
  }
  /* A thin edge of light on one side of a drawn shape (drop-shadow trick). */
  function rim(node, color, dx, dy) { node.style.filter = 'drop-shadow(' + (dx || -2) + 'px ' + (dy || 0) + 'px 0 ' + color + ')'; }
  E.rig = rig; E.gait = gait; E.rim = rim;

  window.PH = E;
})();
