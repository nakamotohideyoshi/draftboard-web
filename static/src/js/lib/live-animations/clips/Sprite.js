export default class Sprite {

  static get FRAME_RATE() {
    return 30;
  }

  constructor() {
    this.isFlipped = false;
  }

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
   * Returns the data representing a specified frame.
   */
  getFrameRect(frame, sheetWidth, sheetHeight, frameWidth, frameHeight) {
    const numCols = sheetWidth / frameWidth;
    let col = frame % numCols;

    // When frame % numCols returns zero, this means that the frame evenly
    // divides into the number of columns and should actually be the last frame
    // of the sequence.
    if (col === 0) {
      col = numCols;
    }

    const row = Math.ceil(frame / numCols);
    const x = (col - 1) * frameWidth;
    const y = (row - 1) * frameHeight;

    return { frame, x, y, width: frameWidth, height: frameHeight, numCols, col, row };
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
  renderFrames(image, canvas, frameWidth, frameHeight, start = 1, finish = -1) {
    let curFrame = start;
    const frameRate = Sprite.FRAME_RATE;
    const context = canvas.getContext('2d');
    const targetFrame = finish === -1
      ? this.getNumFrames(image.width, image.height, frameWidth, frameHeight)
      : finish;

    if (!this._isScaled) {
      context.translate(this.isFlipped ? this.canvas.width : 0, 0);
      context.scale(this.isFlipped ? -1 : 1, 1);
      this._isScaled = true;
    }

    return new Promise((resolve) => {
      this.animate(frameRate, () => {
        this.drawFrame(curFrame, image, context, frameWidth, frameHeight);
        const hasNextFrame = curFrame + 1 <= targetFrame;
        if (!hasNextFrame) {
          resolve();
        }
        curFrame++;

        return hasNextFrame;
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
    let count = 0;

    const tick = () => {
      now = window.performance.now();
      elapsed = now - then;

      if (elapsed > fpsInterval) {
        then = now - (elapsed % fpsInterval);
        isPlaying = fn(++count);
      }

      if (isPlaying) {
        window.requestAnimationFrame(tick);
      }
    };

    window.requestAnimationFrame(tick);
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
      img.src = url;
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
   */
  playOnce(start = 1, finish = -1) {
    if (!this.isLoaded()) {
      return Promise.reject('No image data loaded.');
    }

    return this.renderFrames(this.img, this.canvas, this.canvas.width, this.canvas.height, start, finish);
  }
}
