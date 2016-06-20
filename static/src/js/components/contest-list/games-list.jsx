import React from 'react';
import forEach from 'lodash/forEach';
import moment from 'moment';


/**
 * Renders a list of games that a contest contains.
 */
const GamesList = React.createClass({

  propTypes: {
    boxScores: React.PropTypes.object,
    teams: React.PropTypes.object,
  },


  getGameList(games) {
    const gameList = [];

    forEach(games, (game) => {
      // do we have teams?
      if (this.props.teams.hasOwnProperty('teams')) {
        gameList.push(
          <tr key={game.srid}>
            <td className="teams">
              {this.props.teams.teams[game.srid_away].alias}&nbsp;vs&nbsp;
              {this.props.teams.teams[game.srid_home].alias}
            </td>
            <td className="time">{moment(game.start, moment.ISO_8601).format('h:mma')}</td>
          </tr>
        );
      }
    });

    return gameList;
  },


  render() {
    if (!this.props.boxScores) {
      return (
        <div>Loading...</div>
      );
    }

    return (
      <div className="cmp-games-list">

        <table className="table">
          <thead>
            <tr>
              <th className="place">Teams</th>
              <th className="prize">Time</th>
            </tr>
          </thead>
          <tbody>
            {this.getGameList(this.props.boxScores)}
          </tbody>
        </table>
      </div>
    );
  },

});


module.exports = GamesList;
