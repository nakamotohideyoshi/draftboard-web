import Sprite from '../Sprite';

export default class NBAClip {

  static get FILE_PATH() {
    return '/nba/live-animations';
  }

  constructor(data) {
    this.data = data;
    this._curFrame = 1;
    this.sprite = new Sprite();
  }

  get file() {
    return `${window.dfs.playerImagesBaseUrl}${NBAClip.FILE_PATH}/${this.data.file}`;
  }

  get width() {
    return this.data.frame_width;
  }

  get height() {
    return this.data.frame_height;
  }

  get curFrame() {
    return this._curFrame;
  }

  set curFrame(value) {
    this._curFrame = value;
  }

  get offsetX() {
    const value = this.data.offset_x * 0.5; // Cut it in half for high density displays
    return this.sprite.isFlipped ? this.width - value : value;
  }

  get offsetY() {
    return this.data.offset_y * 0.5; // Cut it in half for high density displays
  }

  get length() {
    return this.data.length;
  }

  get avatars() {
    return this.data.avatars;
  }

  get avatarIn() {
    return this.data.avatar_in;
  }

  avatar(name) {
    return this.data.avatars.find(avatar => avatar.name === name) || null;
  }

  getCuePoint(name) {
    return this.data.cuepoints[name] || 1;
  }

  getElement() {
    return this.sprite.getElement();
  }

  flip(flop = false) {
    this.sprite.isFlipped = flop ? false : !this.sprite.isFlipped;
  }

  load(cuePoint = '') {
    this._curFrame = this.getCuePoint(cuePoint);
    return this.sprite.load(this.file, this.width, this.height).then(() => this);
  }

  play(stop = -1, start = -1) {
    const startFrame = start === -1 ? this._curFrame : start;
    this._curFrame = stop === -1 ? this.length : stop;
    return this.sprite.playOnce(startFrame, this.curFrame).then(() => this);
  }
}
