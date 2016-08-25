export default class Sprite {

  /**
   * Returns the number of frames found in the spritesheet based
   * on the provided frame width and height.
   */
  getNumFrames(sheetWidth, sheetHeight, frameWidth, frameHeight) {
    const cols = Math.floor(sheetWidth / frameWidth);
    const rows = Math.floor(sheetHeight / frameHeight);
    return rows * cols;
  }

  /**
   * Returns the x, y coordinates of the frame
   */
  getFrameRect(frame, sheetWidth, sheetHeight, frameWidth, frameHeight) {
    const numCols = sheetWidth / frameWidth;
    const col = frame % numCols;
    const row = Math.ceil(frame / numCols);

    return {
      x: (col * frameWidth) - frameWidth,
      y: (row * frameHeight) - frameHeight,
      width: frameWidth,
      height: frameHeight,
    };
  }

  /**
   * Draws a single frame from the image into the provided context.
   */
  drawFrame(frame, image, context, frameWidth, frameHeight) {
    const rect = this.getFrameRect(frame, image.width, image.height, frameWidth, frameHeight);
    const targetContext = context;
    targetContext.globalCompositeOperation = 'copy';
    targetContext.drawImage(image, rect.x, rect.y, frameWidth, frameHeight, 0, 0, frameWidth, frameHeight);
  }

  /**
   * Render all the frames.
   */
  renderFrames(image, canvas, frameWidth, frameHeight, flip = false) {
    const frameRate = 29.97;
    const numFrames = this.getNumFrames(image.width, image.height, frameWidth, frameHeight);
    const context = canvas.getContext('2d');
    let curFrame = 1;

    context.translate(flip ? this.canvas.width : 0, 0);
    context.scale(flip ? -1 : 1, 1);

    return new Promise((resolve) => {
      this.animate(frameRate, () => {
        this.drawFrame(curFrame, image, context, frameWidth, frameHeight);
        if (++curFrame < numFrames) {
          return true;
        }

        resolve();
        return false;
      });
    });
  }

  /**
   * Throttles an animation callback at a specified FPS.
   * @param {number}      The target frame rate.
   * @param {function}    The callback to trigger at the specified FPS.
   */
  animate(fps, fn) {
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

    tick();
  }

  /**
   * Loads the sprite for playback.
   * @param {string}  Url to the spritesheet.
   * @param {number}  Width of each individual frame.
   * @param {number}  Height of each individual frame.
   * @return {Promise}
   */
  load(url, frameWidth, frameHeight) {
    const loadSpriteSheet = () => new Promise((resolve, reject) => {
      const img = document.createElement('img');
      img.addEventListener('load', () => resolve(img));
      img.addEventListener('error', () => reject(`Unable to load sprite "${url}"`));
      img.src = `${window.dfs.playerImagesBaseUrl}${url}`;
    });

    const createCanvasFromImg = img => new Promise((resolve) => {
      const canvas = document.createElement('canvas');
      canvas.width = frameWidth;
      canvas.height = frameHeight;
      canvas.style.width = `${frameWidth * 0.5}px`;
      canvas.style.height = `${frameHeight * 0.5}px`;
      return resolve([img, canvas]);
    });

    return loadSpriteSheet().then(createCanvasFromImg).then(([img, canvas]) => {
      this.img = img;
      this.canvas = canvas;
      return Promise.resolve(this);
    });
  }

  /**
   * Returns true if the sprite is ready for playback.
   */
  isLoaded() {
    return this.img || !this.canvas;
  }

  /**
   * Returns the HTML element for displaying the sprite.
   */
  getElement() {
    return this.canvas;
  }

  /**
   * Plays through the animation once.
   * @param {boolean}     Draw each frame flipped horizontally.
   */
  playOnce(flip = false) {
    if (!this.isLoaded()) {
      Promise.reject('No image data loaded.');
    }

    return this.renderFrames(this.img, this.canvas, this.canvas.width, this.canvas.height, flip);
  }
}
