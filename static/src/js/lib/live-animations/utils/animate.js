/**
 * Throttles an animation callback at a specified FPS.
 * @param {number}      The target frame rate.
 * @param {function}    The callback to trigger at the specified FPS.
 */
export default (fps, fn) => {
  const fpsInterval = 1000 / fps;
  let then = window.performance.now();
  let now = then;
  let elapsed = 0;
  let isPlaying = true;

  const tick = () => {
    now = window.performance.now();
    elapsed = now - then;

    if (elapsed > fpsInterval) {
      then = now - (elapsed % fpsInterval);
      isPlaying = fn();
    }

    if (isPlaying) {
      window.requestAnimationFrame(tick);
    }
  };

  window.requestAnimationFrame(tick);
};
