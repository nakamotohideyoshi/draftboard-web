import NBAPlayRecapVO from '../../lib/live-animations/nba/NBAPlayRecapVO';

const PBP_DATA = require('./debug_pbp.json');
export default class PBPFactory {

  constructor() {
    this.recaps = PBP_DATA
      .map(obj => new NBAPlayRecapVO(obj.eventObj))
      .sort((a, b) => {
        if (a.playType() < b.playType()) return -1;
        if (a.playType() > b.playType()) return 1;
        return 0;
      });
    this.curIndex = 0;
    this.whichSide = 'mine';
    this.curEvent = this.recaps[this.curIndex];
    this.onChange = () => {};
  }

  prev() {
    this.goto(this.curIndex - 1);
  }

  next() {
    this.goto(this.curIndex + 1);
  }

  replay() {
    this.goto(this.curIndex);
  }

  goto(index) {
    this.curEvent = this.recaps[index];

    if (this.curEvent) {
      this.curIndex = index;
      this.curEvent._obj.whichSide = this.whichSide;
      this.curEvent._obj.id = new Date().getTime();
      this.onChange(this.curEvent._obj);
    }
  }

  getCurIndex() {
    return this.curIndex;
  }

  getCurEventObj() {
    return this.curEvent._obj;
  }

  setWhichSide(side = 'mine') {
    this.whichSide = side;
    this.goto(this.curIndex);
  }
}
