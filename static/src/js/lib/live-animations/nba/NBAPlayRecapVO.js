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

  static get BLOCK() {
    return 'block';
  }

  static get BLOCKEDDUNK() {
    return 'blockeddunk';
  }

  static get DUNK() {
    return 'dunk';
  }

  static get FIELDGOAL() {
    return 'fieldgoal';
  }

  static get FREETHROW() {
    return 'freethrowmade';
  }

  static get JUMPSHOT() {
    return 'jump shot';
  }

  static get LAYUP() {
    return 'layup';
  }

  static get REBOUND() {
    return 'rebound';
  }

  static get TURNOVER() {
    return 'turnover';
  }

  constructor(data) {
    this._obj = data;
  }

  shot() {
    if (!this._obj.pbp.statistics) {
      return null;
    }

    const block = this._obj.pbp.statistics.find(stat =>
      stat.type === 'block' || stat.type === 'blockeddunk'
    );

    const dunk = this._obj.pbp.statistics.find(stat =>
      stat.type === 'fieldgoal' && stat.shot_type === 'dunk'
    );

    const isMissedShot = this._obj.pbp.event_type.indexOf('miss') !== -1;

    if (block) {
      if (dunk) {
        block.type = 'blockeddunk';
      }

      return block;
    }

    if (isMissedShot) {
      return null;
    }

    return this._obj.pbp.statistics.find(stat => stat.type !== 'assist');
  }

  /**
   * Returns the type of recap depicted. Recap types are determined by
   * evaluating the play by play data and returning the most relevent
   * object type.
   */
  playType() {
    const shot = this.shot();

    // If there's no shot associated with the recap, return the
    // objects event type.
    if (shot === null) {
      return this._obj.pbp.event_type;
    }

    return shot.type === NBAPlayRecapVO.FIELDGOAL ? shot.shot_type : shot.type;
  }

  /**
   * DFS specific value indicating who (fantasy team owner) scored
   * points on the recap.
   */
  whichSide() {
    return this._obj.whichSide;
  }

  /**
   * The side of the court the recap is depicted on.
   */
  courtSide() {
    return this._obj.pbp.attribution.team_basket;
  }

  /**
   * Returns the player's x/y position on the court.
   * @return {Number} The coordinates of the player.
   */
  courtPosition() {
    return {
      x: this._obj.pbp.location__list.coord_x / NBAPlayRecapVO.COURT_LENGTH_INCHES,
      y: this._obj.pbp.location__list.coord_y / NBAPlayRecapVO.COURT_WIDTH_INCHES,
    };
  }
}
