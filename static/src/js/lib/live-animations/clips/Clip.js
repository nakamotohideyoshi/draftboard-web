import Sprite from './Sprite';

export default class Clip {

  constructor(data) {
    this.data = data;
    this._curFrame = 1;
    this.sprite = new Sprite();

    this._el = document.createElement('SPAN');
    this._el.className = 'la-clip';
    this._el.style.position = 'relative';
    this._el.style.display = 'inline-block';
    this._el.style.width = `${this.width * 0.5}px`;
    this._el.style.height = `${this.height * 0.5}px`;
  }

  debug() {
    const debugPoints = [
      [0, 0, '#FF0000'],
      [this.registrationX, this.registrationY, '#00FF00'],
    ];

    this.data.avatars.forEach(avatarPos => {
      let x = avatarPos.x;

      if (this.isFlipped()) {
        x = this.data.frame_width - x;
      }
      debugPoints.push([x * 0.5, avatarPos.y * 0.5, '#CCCCCC']);

      if (this.clipData.pass) {
        debugPoints.push([this.clipData.pass[0], this.clipData.pass[1], '#FFFF00']);
      }
    });

    debugPoints.forEach((pt) => {
      const marker = document.createElement('SPAN');
      marker.style.borderRadius = '4px';
      marker.style.position = 'absolute';
      marker.style.top = `${pt[1] - 2}px`;
      marker.style.left = `${pt[0] - 2}px`;
      marker.style.width = '4px';
      marker.style.height = '4px';
      marker.style.backgroundColor = pt[2];
      this._el.appendChild(marker);
    });

    this._el.style.border = '1px solid rgba(0, 255, 0, .5)';
  }

  get frameWidth() {
    return this.data.frame_width;
  }

  get frameHeight() {
    return this.data.frame_height;
  }

  get screenWidth() {
    return this.data.frame_width * 0.5;
  }

  get screenHeight() {
    return this.data.frame_height * 0.5;
  }

  get registrationX() {
    const xpos = this.data.registration_x * 0.5;
    return !this.sprite.isFlipped ? xpos : this.screenWidth - xpos;
  }

  get registrationY() {
    return this.data.registration_y * 0.5;
  }

  get length() {
    return this.data.length;
  }

  get clipData() {
    return this.data.data || {};
  }

  getFile(name) {
    return this.data.files[name];
  }

  getElement() {
    return this._el;
  }

  flipH() {
    this.sprite.isFlipped = !this.sprite.isFlipped;
  }

  isFlipped() {
    return this.sprite.isFlipped;
  }

  load(file = 'mine') {
    this._curFrame = 1;
    this.debug();
    const fileUri = this.getFile(file);
    return this.sprite.load(fileUri, this.frameWidth, this.frameHeight).then(() => {
      this._el.appendChild(this.sprite.getElement());
    });
  }

  /**
   * Plays the clip to the specified frame. Optionally it can be started from
   * a specified frame.
   */
  playTo(stop = -1, start = -1) {
    const stopFrame = stop === -1 ? this.length : stop;
    const startFrame = start === -1 ? this._curFrame : start;

    // Record the final frame as the clip's current frame. This allows the clip
    // to be resumed.
    this._curFrame = stop;

    return this.sprite.playOnce(startFrame, stopFrame).then(() => this);
  }
}
