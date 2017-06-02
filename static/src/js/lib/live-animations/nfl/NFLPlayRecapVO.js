import _ from 'lodash';

/**
 * Convert yardline to decimal, used by transposeFieldPosition
 * @param  {number} yardline  Range of -10 to 110, represents yardline in NFL
 * @param  {string} direction Direction of drive from user's perspective, options are ['leftToRight', 'rightToLeft']
 * @return {number}           Range of -0.05 to 1.05
 */
function yardlineToDecimal(yardline, driveDirection) {
  let asDecimal = yardline / 100;

  // inverse if away team
  if (driveDirection === 'leftToRight') {
    asDecimal = 1 - asDecimal;
  }

  if (asDecimal > 1) return 1;  // touchdown
  if (asDecimal < 0) return 0;  // touchback
  return asDecimal;
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

  static get PASS_DEEP() {
    return 'pass_deep';
  }

  /**
   * The starting yard line of the play.
   */
  startingYardLine() {
    const yardline = _.get(this._obj, 'pbp.start_situation.location.yardline', 0);
    return yardlineToDecimal(yardline, this.driveDirection());
  }

  /**
   * The ending yard line of the play.
   */
  endingYardLine() {
    const yardline = _.get(this._obj, 'pbp.end_situation.location.yardline', 0);
    return yardlineToDecimal(yardline, this.driveDirection());
  }

  /**
   * The total yards of the play.
   */
  totalYards() {
    return Math.abs(this.endingYardLine() - this.startingYardLine());
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
    } else if (this.isHandOff()) {
      return NFLPlayRecapVO.HANDOFF;
    } else if (this.isPassingPlay()) {
      return this.passType();
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
    } else if (this.passDistance() > 0.2) {
      return NFLPlayRecapVO.PASS_DEEP;
    }
    return NFLPlayRecapVO.PASS;
  }

  /**
   * The distance of the pass in yards.
   * @return {number}
   */
  passDistance() {
    if (!this.isPassingPlay()) {
      return 0;
    }

    if (this.isTurnover()) {
      // Return the distance the defensmen would have intercepted
      // the ball at, before running backwards.
      return Math.abs(this.totalYards() + this.rushDistance());
    }

    // The passing distance is the forward progress minus any
    // additional rushing distance.
    return Math.abs(this.totalYards() - this.rushDistance());
  }

  /**
   * The distance the ball was carried. For passing plays this will
   * be the distance the ball was carried after the catch.
   * @return {number}
   */
  rushDistance() {
    if (this.isPassingPlay()) {
      // Convert the yardsAfterCatch to a float that matches the
      // format of the yardlineStart property. This makes
      // it easy to determine where a catch occurs by subtracting
      // the yardlineEnd() by the rushDistance().
      return yardlineToDecimal(_.get(this._obj, 'pbp.statistics.receive__list.yards_after_catch', 0));
    } else if (this.isRushingPlay()) {
      return this.totalYards();
    }
    return 0;
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
      side = this._obj.pbp.extra_info.rush.side;
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
