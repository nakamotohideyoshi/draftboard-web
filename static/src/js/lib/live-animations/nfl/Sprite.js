export default class Sprite {

    /**
     * Returns the number of frames found in the spritesheet based
     * on the provided frame width and height.
     */
    getNumFrames (sheetWidth, sheetHeight, frameWidth, frameHeight) {
        let cols = Math.floor(sheetWidth / frameWidth);
        let rows = Math.floor(sheetHeight / frameHeight);
        return rows * cols;
    }

    /**
     * Returns the x, y coordinates of the frame
     */
    getFrameRect (frame, sheetWidth, sheetHeight, frameWidth, frameHeight) {
        let numCols = sheetWidth / frameWidth;
        let col = frame % numCols;
        let row = Math.ceil(frame / numCols);

        return {
            x: (col * frameWidth) - frameWidth,
            y: (row * frameHeight) - frameHeight,
            width: frameWidth,
            height: frameHeight
        };
    }

    /**
     * Draws a single frame from the image into the provided context.
     */
    drawFrame (frame, image, context, frameWidth, frameHeight) {
        let rect = this.getFrameRect(frame, image.width, image.height, frameWidth, frameHeight);
        context.globalCompositeOperation = 'copy';
        context.drawImage(image, rect.x, rect.y, frameWidth, frameHeight, 0, 0, frameWidth, frameHeight);
    }

    /**
     * Render all the frames.
     */
    renderFrames (image, canvas, frameWidth, frameHeight, flip = false) {
        let frameRate = 29.97;
        let numFrames = this.getNumFrames(image.width, image.height, frameWidth, frameHeight);
        let curFrame = 1;
        let context = canvas.getContext('2d');

        context.translate(flip ? this.canvas.width : 0, 0);
        context.scale(flip ? -1 : 1, 1);

        return new Promise((resolve, reject) => {
            this.animate(frameRate, () => {
                this.drawFrame(curFrame, image, context, frameWidth, frameHeight);
                if (++curFrame < numFrames) {
                    return true;
                } else {
                    resolve();
                    return false;
                }
            });
        });
    }

    /**
     * Throttles an animation callback at a specified FPS.
     * @param {number}      The target frame rate.
     * @param {function}    The callback to trigger at the specified FPS.
     */
    animate (fps, fn) {
        let fpsInterval = 1000 / fps;
        let isPlaying = true;
        let then = window.performance.now();
        let now = then;
        let elapsed = 0;

        let tick = () => {
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
    load (url, frameWidth, frameHeight) {

        let loadSpriteSheet = () => new Promise((resolve, reject) => {
            let img = document.createElement('img');
            img.addEventListener('load', (e) => resolve(img));
            img.addEventListener('error', (e) => reject(`Unable to load sprite "${url}"`));
            img.src = `${window.dfs.playerImagesBaseUrl}${url}`;
        });

        let createCanvasFromImg = img => new Promise((resolve, reject) => {
            let canvas = document.createElement('canvas');
            canvas.width = frameWidth;
            canvas.height = frameHeight;
            canvas.style.width = `${frameWidth * .5}px`;
            canvas.style.height = `${frameHeight * .5}px`;
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
    isLoaded () {
        return this.img || !this.canvas;
    }

    /**
     * Returns the HTML element for displaying the sprite.
     */
    getElement () {
        return this.canvas;
    }

    /**
     * Plays through the animation once.
     * @param {boolean}     Draw each frame flipped horizontally.
     */
    playOnce (flip = false) {

        if (!this.isLoaded()) {
            Promise.reject('No image data loaded.');
        }

        return this.renderFrames(this.img, this.canvas, this.canvas.width, this.canvas.height, flip);
    }
}
