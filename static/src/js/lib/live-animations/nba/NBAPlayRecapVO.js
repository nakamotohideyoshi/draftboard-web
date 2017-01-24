/**
 *  Value object representing a play recap.
 */
export default class NBAPlayRecapVO {

  static get COURT_LENGTH_INCHES() {
    return 1128;
  }

  static get COURT_WIDTH_INCHES() {
    return 600;
  }

  static get COURT_SIDE_LEFT() {
    return 'left';
  }

  static get COURT_SIDE_RIGHT() {
    return 'right';
  }

  static get BLOCKED_DUNK() {
    return 'blocked_dunk';
  }

  static get BLOCKED_JUMPSHOT() {
    return 'blocked_jumpshot';
  }

  static get FREETHROW() {
    return 'freethrow';
  }

  static get DUNK() {
    return 'dunk';
  }

  static get JUMPSHOT() {
    return 'jumpshot';
  }

  static get LAYUP() {
    return 'layup';
  }

  static get REBOUND() {
    return 'rebound';
  }

  static get STEAL() {
    return 'steal';
  }

  static get UNKNOWN_PLAY() {
    return 'unknown_play';
  }

  constructor(data) {
    this._obj = data;
  }

  /**
   * Returns the type of recap depicted. Recap types are determined by
   * evaluating the play by play data and returning the most relevent
   * play type.
   *
   * @return {String} The type of play.
   */
  playType() {
    const stats = this._obj.pbp.statistics__list;

    if (!stats) {
      return NBAPlayRecapVO.UNKNOWN_PLAY;
    }

    // Evaluate the PBP object's "statistics__list" object for relevant play
    // information. Looking for specific statistic objects gives us the most
    // accurate picture of what happend during the play. Check out SportsRadar
    // API documentation for a full description of the objects within the
    // stats object.

    const hasFreeThrow = stats.hasOwnProperty('freethrow__list');
    const hasBlock = stats.hasOwnProperty('block__list');
    const hasRebound = stats.hasOwnProperty('rebound__list');
    const hasFieldGoal = stats.hasOwnProperty('fieldgoal__list');
    const hasSteal = stats.hasOwnProperty('steal__list');

    if (hasFreeThrow && stats.freethrow__list.made) {
      return NBAPlayRecapVO.FREETHROW;
    }

    if (hasRebound) {
      return NBAPlayRecapVO.REBOUND;
    }

    if (hasSteal) {
      return NBAPlayRecapVO.STEAL;
    }

    if (hasFieldGoal) {
      // Handle missed field goals that are not blocked. Everything else is
      // either a made shot or a blocked shot.
      if (!hasBlock && !stats.fieldgoal__list.made) {
        return NBAPlayRecapVO.UNKNOWN_PLAY;
      }

      switch (stats.fieldgoal__list.shot_type) {
        case 'dunk' :
          return hasBlock
            ? NBAPlayRecapVO.BLOCKED_DUNK
            : NBAPlayRecapVO.DUNK;
        case 'layup' :
          return hasBlock
            ? NBAPlayRecapVO.UNKNOWN_PLAY
            : NBAPlayRecapVO.LAYUP;
        case 'jump shot' :
          return hasBlock
            ? NBAPlayRecapVO.BLOCKED_JUMPSHOT
            : NBAPlayRecapVO.JUMPSHOT;
        default:
      }
    }

    return NBAPlayRecapVO.UNKNOWN_PLAY;
  }

  /**
   * DFS specific value indicating who (fantasy team owner) scored
   * points on the recap.
   * @return {String} Who's lineup contains the play.
   */
  whichSide() {
    return this._obj.whichSide;
  }

  /**
   * The side of the court the recap is depicted on.
   * @return {String} The side of the court the play takes place on.
   */
  courtSide() {
    return this.whichSide() === 'mine' || this.whichSide() === 'both'
      ? NBAPlayRecapVO.COURT_SIDE_LEFT
      : NBAPlayRecapVO.COURT_SIDE_RIGHT;
  }

  /**
   * Returns the play's x/y position on the court.
   * @return {Number} The coordinates of the player.
   */
  courtPosition() {
    return {
      x: this._obj.pbp.location__list.coord_x / NBAPlayRecapVO.COURT_LENGTH_INCHES,
      y: this._obj.pbp.location__list.coord_y / NBAPlayRecapVO.COURT_WIDTH_INCHES,
    };
  }
}
