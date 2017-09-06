/**
 * Throttles an animation callback at a specified FPS.
 * @param {number}      The target frame rate.
 * @param {function}    The callback to trigger at the specified FPS.
 */
const animate = (fps, fn, startingFrame = 1) => {
  const fpsInterval = 1000 / fps;
  let then = window.performance.now();
  let now = then;
  let elapsed = 0;
  let isPlaying = true;
  let frame = startingFrame;

  const tick = () => {
    now = window.performance.now();
    elapsed = now - then;

    if (elapsed > fpsInterval) {
      then = now - (elapsed % fpsInterval);
      isPlaying = fn(frame++);
    }

    if (isPlaying) {
      window.requestAnimationFrame(tick);
    }
  };

  window.requestAnimationFrame(tick);
};

export class Timeline {

  constructor() {
    this._fps = 30;
    this._timelines = [];
    this._onComplete = null;
  }

  add(timeline) {
    this._timelines.push(timeline);
  }

  pause() {
    this._isPaused = true;
  }

  resume() {
    if (this._isPaused) {
      this._isPaused = false;
      this.play(this._onComplete, this._curFrame, this._fps);
    }
  }

  play(onComplete = null, startingFrame = 1, fps = 30) {
    this._isPaused = false;
    this._curFrame = startingFrame;
    this._onComplete = onComplete;
    this._fps = fps;

    const hasNextFrame = (timeline, frame) => {
      const { from, to, length } = timeline;
      const numFrames = length || (to - from + 1);
      const relativeFrame = frame - from + 1;
      const stop = from + numFrames;

      if (timeline.onStart && from === frame) {
        timeline.onStart();
      }

      if (timeline.onUpdate && from <= frame && stop > frame) {
        timeline.onUpdate(relativeFrame, numFrames, frame);
      }

      if (timeline.onComplete && relativeFrame === numFrames) {
        timeline.onComplete();
      }

      return relativeFrame < numFrames;
    };

    animate(this._fps, (curFrame) => {
      let isPlaying = false;
      this._curFrame = curFrame;

      if (this._isPaused) {
        return false;
      }

      for (let i = 0; i < this._timelines.length; i++) {
        if (hasNextFrame(this._timelines[i], curFrame)) {
          isPlaying = true;
        }
      }

      if (!isPlaying && onComplete) {
        onComplete();
      }

      return isPlaying;
    }, this._curFrame);
  }
}

export default animate;
