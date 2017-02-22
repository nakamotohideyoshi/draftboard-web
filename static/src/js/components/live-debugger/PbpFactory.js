import NBAPlayRecapVO from '../../lib/live-animations/nba/NBAPlayRecapVO';
import _ from 'lodash';
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
    this.curIndex = -1;
    this.whichSide = 'mine';
    this.curEvent = this.recaps[this.curIndex];
    this.onChange = () => {};
  }

  hasPrev() {
    return this.curIndex > 0;
  }

  hasNext() {
    return this.curIndex < this.recaps.length;
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
    const maxIndex = this.recaps.length - 1;
    const newIndex = Math.max(0, Math.min(maxIndex, index));

    this.curIndex = newIndex;
    this.curEvent = _.cloneDeep(this.recaps[this.curIndex]._obj);

    // Randomize ID so the event is considered "new"
    this.curEvent.id = `${new Date().getTime()}-${Math.round(Math.random() * 10000)}`;

    // Override the whichSide property with our user defined setting.
    this.curEvent.whichSide = this.whichSide;

    this.onChange(this.curEvent);
  }

  getCurIndex() {
    return this.curIndex;
  }

  getCurEventObj() {
    return this.curEvent;
  }

  setWhichSide(side = 'mine') {
    this.whichSide = side;
    this.goto(this.curIndex);
  }
}
