/* Example Motion scene module (modules/scene-room.js), written against a series lock.
   The scene places the series' cast in the series' set and lights it for its own beat;
   every SERIES.* name comes from the lock (lint check U7). Copy how it is built, never its content. */
kit.scene('room', {
  init(kit) {
    this.set = SERIES.sets.room(kit);
    this.lamp = SERIES.light.lamp(kit, { x: 0.3, y: 0.5, parent: this.set.cam, before: this.set.figures, flicker: 0.03 });
    this.walker = SERIES.cast.walker(kit, this.set.figures, { x: 1430, y: 820, h: 300, facing: -1 });
    this.motes = SERIES.living.motes(kit, { x: 400, y: 300, w: 400, h: 400 });
    this.cam = SERIES.lens.still(kit, this.set.cam);
    SERIES.frame(kit);
  },
  render(t) {
    this.cam.apply(t);
    var g = PH.gait(t, 1, 4, 1430, 1100, 6);
    this.walker.pose({ x: g.x, stride: g.swing * 14, breath: 0.01 * Math.sin(t * 1.8) });
    this.lamp.render(t); this.motes.render(t);
    SERIES.finish(kit, t);
  }
});
