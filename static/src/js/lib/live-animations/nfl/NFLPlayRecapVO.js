import _ from 'lodash';
import { flipOperator } from '../utils/flipPos';

function yardlineToDecimal(yardline) {
  return yardline / 100;
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

  static get SCAMBLE() {
    return 'scramble';
  }

  static get HANDOFF() {
    return 'handoff';
  }

  static get HANDOFF_SHORT() {
    return 'handoff_short';
  }

  static get PASS_DEEP() {
    return 'pass_deep';
  }

  /**
   * The starting yard line of the play.
   */
  startingYardLine() {
    let yardline = _.get(this._obj, 'pbp.start_situation.location.yardline', 0);
    const possession = this._obj.pbp.start_situation.possession.alias;
    const sideOfField = this._obj.pbp.start_situation.location.alias;
    const isGoingRightToLeft = this.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT;

    if (sideOfField !== possession && !isGoingRightToLeft) {
      yardline = 100 - yardline;
    } else if (sideOfField === possession && isGoingRightToLeft) {
      yardline = 100 - yardline;
    }

    return yardlineToDecimal(yardline);
  }

  /**
   * The ending yard line of the play.
   */
  endingYardLine() {
    // Calculate the endingYardLine based on the total passing & rushing yards
    // accrued during the play to ensure that plays that cross the 50 yardline
    // are properly displayed.
    const isFlipped = this.driveDirection() === NFLPlayRecapVO.RIGHT_TO_LEFT;
    return flipOperator(this.startingYardLine(), '+', this.totalYards(), isFlipped);
  }

  /**
   * The distance of the pass in yards.
   * @return {number}
   */
  passingYards() {
    const yards = _.get(this._obj, 'pbp.statistics.pass__list.att_yards', 0);
    return yardlineToDecimal(yards);
  }

  /**
   * The distance the ball was carried. For passing plays this will
   * be the distance the ball was carried after the catch.
   * @return {number}
   */
  rushingYards() {
    const yards = this.isPassingPlay()
    ? _.get(this._obj, 'pbp.statistics.receive__list.yards_after_catch', 0)
    : _.get(this._obj, 'pbp.statistics.rush__list.yards', 0);

    return yardlineToDecimal(yards);
  }

  /**
   * The total yards of the play.
   */
  totalYards() {
    return this.passingYards() + this.rushingYards();
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
    return this._obj.pbp.type;
  }

  /**
   * The plays description.
   * @return {string}
   */
  playDescription() {
    return this._obj.pbp.description;
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
      if (this.totalYards() === 0) {
        return NFLPlayRecapVO.HANDOFF;
      } else if (this.totalYards() < 0.03) {
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
    return this.whichSide() === 'mine' || this.whichSide() === 'both'
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
   * Returns an array of info for all players featured in the recap.
   */
  players() {
    const stats = this._obj.pbp.statistics;

    return [
      { stat: 'pass__list', player: 'quarterback' },
      { stat: 'receive__list', player: 'receiver' },
      { stat: 'rush__list', player: 'receiver' },
    ].filter(
      list => stats.hasOwnProperty(list.stat) && stats[list.stat].hasOwnProperty('player')
    ).map(list => {
      const playerId = stats[list.stat].player;

      const playerStats = this._obj.stats.filter(stat => (
        stat.srid_player === playerId
      ))[0];

      const playerName = `${playerStats.first_name} ${playerStats.last_name}`;

      return { type: list.player, name: playerName, id: playerId };
    });
  }
}
