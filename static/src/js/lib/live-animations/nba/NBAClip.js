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
    return this.data.width;
  }

  get height() {
    return this.data.height;
  }

  get curFrame() {
    return this._curFrame;
  }

  set curFrame(value) {
    this._curFrame = value;
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

  play(stop = -1, start = -1) {
    const startFrame = start === -1 ? this._curFrame : start;
    this._curFrame = stop === -1 ? this.length : stop;
    console.log('NBAClip.play()', startFrame, this._curFrame);
    return this.sprite.playOnce(startFrame, this.curFrame).then(() => this);
  }
}
