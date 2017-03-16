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

  static get BASKET_LEFT() {
    return 'left';
  }

  static get BASKET_RIGHT() {
    return 'right';
  }

  static get BLOCKED_DUNK() {
    return 'blocked_dunk';
  }

  static get BLOCKED_HOOKSHOT() {
    return 'blocked_hookshot';
  }

  static get BLOCKED_JUMPSHOT() {
    return 'blocked_jumpshot';
  }

  static get BLOCKED_LAYUP() {
    return 'blocked_layup';
  }

  static get FREETHROW() {
    return 'freethrow';
  }

  static get DUNK() {
    return 'dunk';
  }

  static get HOOKSHOT() {
    return 'hookshot';
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

    if (stats.hasOwnProperty('freethrow__list')) {
      return NBAPlayRecapVO.FREETHROW;
    }

    if (stats.hasOwnProperty('rebound__list')) {
      return NBAPlayRecapVO.REBOUND;
    }

    if (stats.hasOwnProperty('steal__list')) {
      return NBAPlayRecapVO.STEAL;
    }

    if (!stats.hasOwnProperty('fieldgoal__list')) {
      return NBAPlayRecapVO.UNKNOWN_PLAY;
    }

    const shotType = stats.fieldgoal__list.shot_type;
    const hasBlock = stats.hasOwnProperty('block__list');

    switch (shotType) {
      case 'dunk' :
        return hasBlock
          ? NBAPlayRecapVO.BLOCKED_DUNK
          : NBAPlayRecapVO.DUNK;
      case 'layup' :
        return hasBlock
          ? NBAPlayRecapVO.BLOCKED_LAYUP
          : NBAPlayRecapVO.LAYUP;
      case 'hook shot' :
        return hasBlock
          ? NBAPlayRecapVO.BLOCKED_HOOKSHOT
          : NBAPlayRecapVO.HOOKSHOT;
      case 'jump shot' :
        return hasBlock
          ? NBAPlayRecapVO.BLOCKED_JUMPSHOT
          : NBAPlayRecapVO.JUMPSHOT;
      default:
        return NBAPlayRecapVO.UNKNOWN_PLAY;
    }
  }

  playDescription() {
    return this._obj.pbp.description;
  }

  /**
   * Returns true if the play consists of a made shot.
   */
  madeShot() {
    const stats = this._obj.pbp.statistics__list;

    if (!stats) {
      return false;
    } else if (stats.hasOwnProperty('fieldgoal__list')) {
      return stats.fieldgoal__list.made === 'true';
    } else if (stats.hasOwnProperty('freethrow__list')) {
      return stats.freethrow__list.made === 'true';
    }

    return false;
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
   * Returns the basket the play should be played on. All plays belonging to
   * "mine", or "both", lineups will be shown on the left side of the court, while
   * all other plays will be displayed on the right side of the court.
   * @return {String} The side of the court the play takes place on.
   */
  teamBasket() {
    return this.whichSide() === 'mine' || this.whichSide() === 'both'
      ? NBAPlayRecapVO.BASKET_LEFT
      : NBAPlayRecapVO.BASKET_RIGHT;
  }

  /**
   * Returns the play's x/y position on the court.
   * @return {Number} The coordinates of the play.
   */
  courtPosition() {
    const pos = {
      x: this._obj.pbp.location__list.coord_x / NBAPlayRecapVO.COURT_LENGTH_INCHES,
      y: this._obj.pbp.location__list.coord_y / NBAPlayRecapVO.COURT_WIDTH_INCHES,
    };

    // Do not transform "steals". Steals should be depicted where they happen on
    // the court in real life. Everything else gets tranformed based on which
    // teamBasket the play should be aimed at.
    if (this.playType() === NBAPlayRecapVO.STEAL) {
      return pos;
    }

    // Determine the side of the court the play took place on by evaluating if
    // the x coordinate is over the half court line.
    // Note: This could have undesirable outcomes for plays that take place in
    // the backcourt (steals, turnovers, half court shots). The best solution
    // would be for the team_basket to be specified via the API instead of
    // guestimating it based on the play's position on the court..
    const basket = pos.x > 0.5
      ? NBAPlayRecapVO.BASKET_RIGHT
      : NBAPlayRecapVO.BASKET_LEFT;

    // Flip the x coordinate of the play if the original coordinate does not
    // match our target teamBasket.
    if (this.teamBasket() !== basket) {
      pos.x = 1 - pos.x;
    }

    return pos;
  }

  /**
   * Returns the play's "title" associated with the play's playType.
   */
  playTitle() {
    const playTypeToTitle = {
      [NBAPlayRecapVO.FREETHROW]: 'Freethrow',
      [NBAPlayRecapVO.DUNK]: 'Dunk',
      [NBAPlayRecapVO.BLOCKED_DUNK]: 'Block',
      [NBAPlayRecapVO.BLOCKED_HOOKSHOT]: 'Block',
      [NBAPlayRecapVO.BLOCKED_JUMPSHOT]: 'Block',
      [NBAPlayRecapVO.BLOCKED_LAYUP]: 'Block',
      [NBAPlayRecapVO.JUMPSHOT]: 'Jumpshot',
      [NBAPlayRecapVO.HOOKSHOT]: 'Hookshot',
      [NBAPlayRecapVO.LAYUP]: 'Layup',
      [NBAPlayRecapVO.STEAL]: 'Steal',
      [NBAPlayRecapVO.REBOUND]: 'Rebound',
    };

    const type = this.playType();

    if (!playTypeToTitle.hasOwnProperty(type)) {
      return '';
    }

    return playTypeToTitle[this.playType()];
  }

  /**
   * Returns the relevant player based on the provided player ID.
   */
  relevantPlayerById(playerId) {
    return this._obj.relevantPlayersInEvent.find(playerObj =>
      playerObj.id === playerId
    );
  }

  /**
   * Returns an array of info for all players featured in the recap.
   */
  players() {
    const stats = this._obj.pbp.statistics__list;
    const players = [];

    if (!stats) {
      return players;
    }

    if (stats.hasOwnProperty('block__list')) {
      players.push({ type: 'defense', id: stats.block__list.player });
    } else if (stats.hasOwnProperty('steal__list')) {
      players.push({ type: 'defense', id: stats.steal__list.player });
    }

    if (stats.hasOwnProperty('rebound__list')) {
      players.push({ type: 'rebound', id: stats.rebound__list.player });
    }

    if (stats.hasOwnProperty('fieldgoal__list')) {
      players.push({ type: 'offense', id: stats.fieldgoal__list.player });
    } else if (stats.hasOwnProperty('freethrow__list')) {
      players.push({ type: 'offense', id: stats.freethrow__list.player });
    } else if (stats.hasOwnProperty('turnover__list')) {
      players.push({ type: 'offense', id: stats.turnover__list.player });
    }

    return players.map(playerInfo => {
      const obj = playerInfo;
      obj.name = this._obj.playerNames[obj.id] || '';

      return obj;
    });
  }
}
