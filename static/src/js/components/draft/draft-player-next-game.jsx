import React from 'react';
import find from 'lodash/find';


/**
 * Render a player's next game with their team highlighted. ex: GSW @ *SAS*
 */
const DraftPlayerNextGame = React.createClass({

  propTypes: {
    game: React.PropTypes.object,
    highlightTeamSrid: React.PropTypes.string,
  },


  shouldComponentUpdate(nextProps) {
    // Only update if we don't have any game info, but are getting some.
    return !this.props.game && nextProps.game !== 'undefined';
  },


  render() {
    if (this.props.game && this.props.game.homeTeam) {
      // get the home + away teams
      const homeTeam = find(this.props.game, { srid: this.props.game.srid_home });
      const awayTeam = find(this.props.game, { srid: this.props.game.srid_away });

      // if this player is on the away team, make that bold.
      if (this.props.highlightTeamSrid === this.props.game.srid_away) {
        return (
          <span><span className="player-team">{awayTeam.alias}</span> @ {homeTeam.alias}</span>
        );
      }
      // Otherwise, they are on the home team, make that bold.
      return (
        <span>{awayTeam.alias} @ <span className="player-team">{homeTeam.alias}</span></span>
      );
    }

    return (
      <span></span>
    );
  },
});


module.exports = DraftPlayerNextGame;
