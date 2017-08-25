import _ from 'lodash';
import NFLPlayDescription from './NFLPlayDescription';

function yardsToDecimal(yardline) {
  return yardline / 100;
}

function mapYardlineToField(yardline, possession, sideOfField, driveDirection) {
  const isGoingRightToLeft = driveDirection === 'rightToLeft';
  const isPastThe50 = possession !== sideOfField;
  const yardlineAsDecimal = yardsToDecimal(yardline);

  if (isPastThe50 && !isGoingRightToLeft) {
    return 1 - yardlineAsDecimal;
  } else if (!isPastThe50 && isGoingRightToLeft) {
    return 1 - yardlineAsDecimal;
  }

  return yardlineAsDecimal;
}

/**
*  Value object representing a play recap.
*/
export default class NFLPlayRecapVO {

  constructor(data) {
    this._obj = data;
  }

  static get LEFT_TO_RIGHT() {
    return 'leftToRight';
  }

  static get RIGHT_TO_LEFT() {
    return 'rightToLeft';
  }

  static get MIDDLE() {
    return 'middle';
  }

  static get RIGHT() {
    return 'right';
  }

  static get LEFT() {
    return 'left';
  }

  static get PASS() {
    return 'pass';
  }

  static get RUSH() {
    return 'rush';
  }

  static get KICKOFF() {
    return 'kickoff';
  }

  static get PUNT() {
    return 'punt';
  }

  static get SCAMBLE() {
    return 'scramble';
  }

  static get HANDOFF() {
    return 'handoff';
  }

  static get HANDOFF_SHORT() {
    return 'handoff_short';
  }

  static get HANDOFF_FUMBLE() {
    return 'handoff_fumble';
  }

  static get PASS_DEEP() {
    return 'pass_deep';
  }

  static get PASS_SHORT() {
    return 'pass_short';
  }

  static get UNKNOWN_PLAY() {
    return 'unknown_play';
  }

  /**
   * The starting yardline of the play.
   */
  startingYardLine() {
    const situation = this._obj.pbp.start_situation;
    const yardline = situation.location.yardline;
    const possession = situation.possession.alias;
    const sideOfField = situation.location.alias;

    return mapYardlineToField(yardline, possession, sideOfField, this.driveDirection());
  }

  /**
   * The ending yard line of the play.
   */
  endingYardLine() {
    const situation = this._obj.pbp.end_situation;
    const yardline = situation.location.yardline;
    const sideOfField = situation.location.alias;
    const possession = situation.possession.alias;

    return mapYardlineToField(yardline, possession, sideOfField, this.driveDirection());
  }

  /**
   * The distance of the pass in yards.
   * @return {number}
   */
  passingYards() {
    const yards = _.get(this._obj, 'pbp.statistics.pass__list.att_yards', 0);
    return yardsToDecimal(yards);
  }

  /**
   * The distance the ball was carried. For passing plays this will
   * be the distance the ball was carried after the catch for kick returns this
   * is the distance the ball was returned.
   * @return {number}
   */
  rushingYards() {
    let yards = 0;
    switch (this.playType()) {
      case NFLPlayRecapVO.PASS:
        yards = _.get(this._obj, 'pbp.statistics.receive__list.yards_after_catch', 0);
        break;
      case NFLPlayRecapVO.RUSH:
        yards = _.get(this._obj, 'pbp.statistics.rush__list.yards', 0);
        break;
      case NFLPlayRecapVO.KICKOFF:
        yards = _.get(this._obj, 'pbp.statistics.return__list.yards', 0);
        break;
      case NFLPlayRecapVO.PUNT:
        yards = _.get(this._obj, 'pbp.statistics.return__list.yards', 0);
        break;
      default:
        return 0;
    }

    return yardsToDecimal(yards);
  }

  /**
   * The total yards the ball was kicked.
   * @return {[type]} [description]
   */
  kickedYards() {
    return yardsToDecimal(_.get(this._obj, 'pbp.punt__list.yards', 0));
  }

  /**
   * ...
   */
  whichSide() {
    return this._obj.whichSide;
  }

  /**
   * The type of play.
   * @return {string}
   */
  playType() {
    const supportedTypes = [
      NFLPlayRecapVO.PASS,
      NFLPlayRecapVO.RUSH,
      NFLPlayRecapVO.KICKOFF,
      NFLPlayRecapVO.PUNT,
    ];

    const type = this._obj.pbp.type;
    return supportedTypes.indexOf(type) !== -1 ? type : NFLPlayRecapVO.UNKNOWN_PLAY;
  }

  /**
   * The plays description.
   * @return {string}
   */
  playDescription() {
    return new NFLPlayDescription(this).toText();
  }

  /**
   * The plays description.
   * @return {string}
   */
  playHTMLDescription() {
    return new NFLPlayDescription(this).toHTML();
  }

  /**
   * Returns the "title" based on the play's playType.
   */
  playTitle() {
    const yards = Math.round(100 * (this.passingYards() + this.rushingYards()));

    if (this.isTouchdown()) {
      return 'Touchdown';
    } else if (this.isTouchback()) {
      return 'Touchback';
    } else if (this.isFumble()) {
      return 'Fumble';
    } else if (this.isTurnover()) {
      return 'Interception';
    } else if (this.isIncompletePass()) {
      return 'Incomplete Pass';
    } else if (this.isQBSack()) {
      return 'Sack';
    } else if (this.playType() === NFLPlayRecapVO.PUNT) {
      return `${yards} Yard Punt Return`;
    } else if (this.playType() === NFLPlayRecapVO.KICKOFF) {
      return `${yards} Yard Kickoff Return`;
    } else if (this.isPassingPlay()) {
      return `${yards} Yard Completion`;
    } else if (this.isRushingPlay()) {
      return `${yards} Yard Rush`;
    }

    return '';
  }

  /**
   * The play formation before the snap.
   * @return {string}
   */
  playFormation() {
    return this._obj.pbp.extra_info.formation;
  }

  /**
   * String representing the Quarterbacks action.
   * @return {string|null}
   */
  qbAction() {
    if (this.isScramble()) {
      return NFLPlayRecapVO.SCAMBLE;
    }

    if (this.isPassingPlay()) {
      return this.passType();
    }

    if (this.isHandOff()) {
      if (this.isFumble()) {
        return NFLPlayRecapVO.HANDOFF_FUMBLE;
      } else if (this.rushingYards() === 0) {
        return NFLPlayRecapVO.HANDOFF;
      } else if (this.rushingYards() < 0.03) {
        return NFLPlayRecapVO.HANDOFF_SHORT;
      }

      return NFLPlayRecapVO.HANDOFF;
    }

    return null;
  }

  /**
   * The type of pass being thrown by quarterback.
   * @return {string}
   */
  passType() {
    if (!this.isPassingPlay()) {
      return null;
    } else if (this.passingYards() > 0.2) {
      return NFLPlayRecapVO.PASS_DEEP;
    } else if (this.passingYards() < 0.1) {
      return NFLPlayRecapVO.PASS_SHORT;
    }
    return NFLPlayRecapVO.PASS;
  }

  /**
   * The side of the field the play finishes on. Possible values are
   * "left", "middle", "right". defaulting to "middle"
   * @return {string}
   */
  side() {
    let side = null;
    if (this.isPassingPlay()) {
      side = this._obj.pbp.extra_info.pass.side;
    } else if (this.isRushingPlay()) {
      side = NFLPlayRecapVO.MIDDLE;
    }
    return side || NFLPlayRecapVO.MIDDLE;
  }

  /**
   * The plays drive direction. Possible values are "rightToLeft"
   * or "leftToRight".
   * @return {string}
   */
  driveDirection() {
    return this.whichSide() !== 'opponent'
      ? NFLPlayRecapVO.LEFT_TO_RIGHT
      : NFLPlayRecapVO.RIGHT_TO_LEFT;
  }

  /**
   * Returns true if the play is an incomplete pass.
   */
  isIncompletePass() {
    return this.isPassingPlay() && _.get(this._obj, 'pbp.statistics.pass__list.complete', 0) === 0;
  }

  /**
   * Returns true if the play resulted in a touchdown.
   */
  isTouchdown() {
    return _.get(this._obj, 'pbp.extra_info.touchdown', false) === true;
  }

  /**
   * Returns true if the QB hands off the ball.
   * @return {boolean}
   */
  isHandOff() {
    return !this.isPassingPlay() && !this.isScramble();
  }

  /**
   * Returns true if the QB sneeks the ball.
   * @return {boolean}
   */
  isScramble() {
    return this.isRushingPlay() && this._obj.pbp.extra_info.rush.scramble;
  }

  /**
   * Returns true if the pass results in an interception or fumble.
   * @return {boolean}
   */
  isTurnover() {
    return this.isPassingPlay() && this._obj.pbp.extra_info.intercepted;
  }

  /**
   * Returns true if the play contains a fumble.
   */
  isFumble() {
    const fumbles = _.get(this._obj, 'pbp.statistics.fumble__list', false);
    return Boolean(fumbles);
  }

  /**
   * Returns true if the play resulted in a safety.
   */
  isSafety() {
    return this._obj.pbp.description.toLowerCase().indexOf('safety') !== -1;
  }

  /**
   * Returns true if the play resulted in a touchback.
   * @return {Boolean}
   */
  isTouchback() {
    return _.get(this._obj, 'pbp.statistics.return__list.touchback', 0) === 1;
  }

  /**
   * Returns true if the QB passes the ball.
   * @return {boolean}
   */
  isPassingPlay() {
    return this.playType() === NFLPlayRecapVO.PASS;
  }

  /**
   * Returns true if the play represents a run only.
   * @return {boolean}
   */
  isRushingPlay() {
    return this.playType() === NFLPlayRecapVO.RUSH;
  }

  /**
   * Returns true if the play represents a quarterback being sacked.
   * @return {boolean}
   */
  isQBSack() {
    return _.get(this._obj, 'pbp.statistics.pass__list.sack', false);
  }

  /**
   * Returns true if the play contains a penalty.
   * @return {boolean}
   */
  hasPenalty() {
    return Boolean(_.get(this._obj, 'pbp.statistics.penalty__list', false));
  }

  /**
   * Returns an array of player objects for all players featured in the recap.
   */
  players() {
    return this._obj.players.map(
      player => _.merge(player, {
        avatarType: this.getPlayerAvatarTypeBySRID(player.srid_player),
        lineup: this.getPlayerLineupById(player.player_id),
      })
    );
  }

  /**
   * Returns the type associated with a player based on the statistical list
   * their SRID is found in i.e(pass__list.player).
   */
  getPlayerAvatarTypeBySRID(srid) {
    const typesByList = [
        { list: 'pbp.statistics.pass__list.player', type: 'quarterback' },
        { list: 'pbp.statistics.receive__list.player', type: 'receiver' },
        { list: 'pbp.statistics.rush__list.player', type: 'receiver' },
        { list: 'pbp.statistics.return__list.player', type: 'receiver' },
    ];

    const player = typesByList.find(playerType => (
      _.get(this._obj, playerType.list) === srid
    ));

    return !player ? 'unknown' : player.type;
  }

  /**
   * Returns the lineup associated with the provided `id`. Returns "none" if
   * the playerId is not associated with any known lineup.
   */
  getPlayerLineupById(id) {
    const { whichSidePlayers } = this._obj;
    const playerWithLineup = whichSidePlayers.find(player => id === player.playerId);
    return !playerWithLineup ? 'none' : playerWithLineup.lineup;
  }
}
