import Sprite from './Sprite';

export default class Clip {

  constructor(data) {
    this.data = data;
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
    });

    this.data.cuepoints.forEach(cuepoint => {
      const { x, y } = cuepoint.data;
      if (x && y) {
        debugPoints.push([x * 0.5, y * 0.5, '#FF00FF']);
      }
    });

    debugPoints.forEach((pt) => {
      const marker = document.createElement('SPAN');
      marker.style.borderRadius = '2px';
      marker.style.position = 'absolute';
      marker.style.top = `${pt[1] - 1}px`;
      marker.style.left = `${pt[0] - 1}px`;
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

  getFile(name) {
    return this.data.files[name];
  }

  /**
   * Returns the Cuepoint with the provided name.
   */
  getCuepoint(name) {
    return this.data.cuepoints.find(cuepoint => cuepoint.name === name);
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
    const fileUri = this.getFile(file);
    return this.sprite.load(fileUri, this.frameWidth, this.frameHeight).then(
      () => {
        this._el.appendChild(this.sprite.getElement());
        return this.sprite.goto(1);
      }
    );
  }

  /**
   * Move the playhead to the specified frame.
   */
  goto(frame) {
    this.sprite.goto(frame);
  }
}
