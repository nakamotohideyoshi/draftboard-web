import _ from 'lodash';
import NBAPlayRecapVO from '../../lib/live-animations/nba/NBAPlayRecapVO';
import NFLPlayRecapVO from '../../lib/live-animations/nfl/NFLPlayRecapVO';


const PBP_DATA = process.env.NODE_ENV === 'test' ? {} : {
  nba: require('./data/pusher_events__zach_local_nba_pbp.event.txt'),
  nfl: require('./data/pusher_events__zach_local_nfl_pbp.linked.txt'),
  nhl: '',
};

const parseNBA = (obj) => {
  const pbp = _.merge(obj, {
    gameId: obj.game__id,
    isBigPlay: true,
    description: obj.pbp.description,
  });

  return new NBAPlayRecapVO(pbp);
};

const parseNFL = (obj) => {
  const pbp = _.merge(_.cloneDeep(obj), {
    gameId: obj.pbp.srid_game,
  });

  return new NFLPlayRecapVO(pbp);
};

export default class PBPFactory {

  constructor(sport) {
    this.onChange = () => {};
    this.loadSport(sport);
  }

  loadSport(sport) {
    const strToJSON = (str) => {
      try {
        return JSON.parse(str);
      } catch (e) {
        return null;
      }
    };

    const messageToRecap = (obj, index) => {
      const message = _.merge(obj, {
        sport,
        id: `pbp-${index}`,
        quarter: 1,
      });

      switch (sport) {
        case 'nba' : return parseNBA(message);
        case 'nfl' : return parseNFL(message);
        default : return message;
      }
    };

    const sortByPlayType = (a, b) => {
      if (a.playType() < b.playType()) return -1;
      if (a.playType() > b.playType()) return 1;
      return 0;
    };

    const parseMessages = (data) => (
      data.map(strToJSON)
      .filter(obj => obj !== null)
      .map(messageToRecap)
      .sort(sortByPlayType)
    );

    this.recaps = parseMessages(PBP_DATA[sport].split('\n'));
    this.curIndex = -1;
    this.curEvent = null;
    this.onChange(this.getCurEventObj(), this.getRecaps());
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

    this.onChange(this.getCurEventObj(), this.getRecaps());
    return this.getCurEventObj();
  }

  gotoPBPById(id) {
    const recaps = this.getRecaps();
    for (let i = 0; i < recaps.length; i++) {
      if (recaps[i]._obj.id === id) {
        return this.goto(i);
      }
    }
  }

  getCurIndex() {
    return this.curIndex;
  }

  getCurEventObj() {
    return this.curEvent;
  }

  getRecaps() {
    return this.recaps;
  }
}
