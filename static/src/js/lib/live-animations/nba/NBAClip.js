import Sprite from '../Sprite';

export default class NBAClip {

  static get FILE_PATH() {
    return '/nba/live-animations';
  }

  constructor(data) {
    this.data = data;
    this.sprite = new Sprite();
  }

  get avatarIn() {
    return this.data.avatar_in;
  }

  get avatarX() {
    return this.data.avatar_x;
  }

  get avatarY() {
    return this.data.avatar_y;
  }

  get file() {
    return `${NBAClip.FILE_PATH}/${this.data.file}`;
  }

  get width() {
    return this.data.width;
  }

  get height() {
    return this.data.height;
  }

  get offsetX() {
    return this.sprite.isFlipped
      ? this.width - this.data.offset_x
      : this.data.offset_x;
  }

  get offsetY() {
    return this.data.offset_y;
  }

  get length() {
    return this.data.length;
  }

  getCuePoint(name) {
    return this.data.cuepoints[name] || 0;
  }

  getElement() {
    return this.sprite.getElement();
  }

  flip(flop = false) {
    this.sprite.isFlipped = flop ? false : !this.sprite.isFlipped;
  }

  load() {
    return this.sprite.load(this.file, this.width, this.height).then(() => this);
  }

  playOnce(start = 1, numFrames = -1) {
    const playLength = numFrames === -1 ? this.length : numFrames;
    return this.sprite.playOnce(start, playLength).then(() => this);
  }
}
