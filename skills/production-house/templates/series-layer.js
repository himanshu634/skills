/* SERIES layer template. Shows the STRUCTURE every series layer follows; its drawing is
   deliberately plain placeholder art. Never reuse its look: every value below is decided
   by the art department from this series' research (references/art-department.md).
   Rules: define functions only at load (no DOM until a scene calls a builder); pure in t;
   colors from var(--ground|--main|--second|--accent). */
(function (E) {
  var S = { id: 'example-series', version: '1.0.0', engine: '2.0' };
  S.look = { name: 'Placeholder', aspect: 0, fps: 24, texture: 0 };   /* from the bible */

  /* Light recipes: named for what they are in the story world. Compose engine primitives,
     return a controller with render(t). Opts always pass parent/before through. */
  S.light = {
    lamp: function (kit, o) {
      o = o || {};
      var at = { parent: o.parent, before: o.before };
      E.shade(kit, Object.assign({ x: o.x, y: o.y, rx: 0.4, ry: 0.3, inner: 0.2, dark: o.dark === undefined ? 0.6 : o.dark }, at));
      var pool = E.pool(kit, Object.assign({ x: o.x, y: o.y, rx: 0.3, ry: 0.24, color: 'var(--accent)' }, at));
      var bulb = E.glow(kit, Object.assign({ x: o.x, y: o.y, size: 36, color: 'var(--accent)' }, at));
      return E.light(kit, Object.assign({ parts: [{ el: pool }, { el: bulb, flick: 0.2 }], keys: o.keys, flicker: o.flicker }, at));
    },
    daylight: function (kit, o) {
      o = o || {};
      var w = E.wash(kit, { parent: o.parent, before: o.before, angle: o.angle || 115, color: 'var(--second)', a0: 30 });
      return E.light(kit, { parts: [{ el: w }], keys: o.keys });
    }
  };

  /* Lens grammar: each mode is a dramatic state (write the meaning in the bible). */
  S.lens = {
    still: function (kit, layers, o) { return E.camera(kit, layers, function () { return { s: 1 }; }, o); },
    drift: function (kit, layers, o) { o = o || {}; var d = kit.dur || 10; return E.camera(kit, layers, function (t) { return { s: 1.04, x: -(o.speed || 10) * (t - d / 2) }; }, o); },
    push: function (kit, layers, o) { o = o || {}; var d = kit.dur || 10; return E.camera(kit, layers, function (t) { return { s: E.lerp(1, o.z1 || 1.1, E.ease.inOut(E.seg(t, o.from || 0, o.to || d))) }; }, o); }
  };

  /* Living elements: what keeps a still picture alive in this world. */
  S.living = {
    motes: function (kit, o) {
      o = o || {};
      return E.particles(kit, { n: o.n || 24, seed: o.seed || 3, init: function (r) { return [r(), r(), 1 + r() * 2]; },
        draw: function (c, p, t) { c.globalAlpha = 0.4; c.fillStyle = 'rgba(255,255,255,1)'; c.beginPath();
          c.arc(o.x + p[0] * o.w, o.y + E.mod1(p[1] - t * 0.02) * o.h, p[2], 0, 6.28); c.fill(); } });
    }
  };

  /* Frame and finish: required; either may be a no-op for this look. */
  S.frame = function (kit) { return E.matte(kit, { aspect: S.look.aspect }); };
  S.finish = function (kit, t) { if (S.look.texture) E.texture(kit, t, { amount: S.look.texture }); };

  /* Cast: each recurring character, built once. Opts: x, y (feet px), h (px), facing.
     Expose pose() in the character's own terms. */
  S.cast = {
    walker: function (kit, svg, o) {
      o = o || {};
      var R = E.rig(kit, svg, { x: o.x, y: o.y, scale: (o.h || 300) / 100, facing: o.facing || 1, fill: 'var(--main)', parts: [
        { id: 'legL', pivot: [-4, -45], draw: 'M-8 -45 h7 v45 h-7 Z' },
        { id: 'legR', pivot: [4, -45], draw: 'M1 -45 h7 v45 h-7 Z' },
        { id: 'body', pivot: [0, -45], draw: 'M-12 -82 h24 v40 h-24 Z' },
        { id: 'head', parent: 'body', pivot: [0, -82], draw: function (g) { E.el('circle', { cx: 0, cy: -92, r: 10 }, g); } }
      ] });
      return { root: R.root, pose: function (p) { p = p || {}; R.pose({ x: p.x, y: p.y, opacity: p.opacity, joints: { legL: p.stride || 0, legR: -(p.stride || 0), head: p.head || 0, body: { sy: 1 + (p.breath || 0) } } }); } };
    }
  };

  /* Sets: each recurring location, built once. Return the layers a scene needs and named
     anchors; lights stay out of sets so each scene lights its own beat. */
  S.sets = {
    room: function (kit) {
      kit.stage.append(kit.h('<div class="ground"></div>'));
      var cam = E.layer(kit, kit.stage, { clip: true }), art = E.svg(kit, cam);
      E.el('rect', { x: 0, y: 820, width: 1920, height: 260, style: 'fill:var(--second);opacity:.35' }, art);
      E.el('rect', { x: 1300, y: 300, width: 260, height: 520, style: 'fill:var(--main);opacity:.5' }, art);
      return { cam: cam, art: art, figures: E.svg(kit, cam), anchors: { floor: 820, door: [1430, 820] } };
    }
  };

  window.SERIES = S;
})(window.PH);
