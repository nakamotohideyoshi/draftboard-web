import Sprite from '../Sprite';

export default class NBAClip {

  static get FILE_PATH() {
    return '/nba/live-animations';
  }

  constructor(data) {
    this.data = data;
    this.sprite = new Sprite();
  }

  get file() {
    return `${window.dfs.playerImagesBaseUrl}${NBAClip.FILE_PATH}/${this.data.file}`;
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

  avatar(name) {
    if (!this.data.avatars.hasOwnProperty(name)) {
      throw new Error(`The requested avatar ${name} is not specified`);
    }

    return this.data.avatars[name];
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

  play(start = 1, stop = -1) {
    const lastFrame = stop === -1 ? this.length : stop;
    return this.sprite.playOnce(start, lastFrame).then(() => this);
  }
}
