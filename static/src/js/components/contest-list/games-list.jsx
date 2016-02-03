import React from 'react';
import { forEach as _forEach } from 'lodash';
import moment from 'moment';


/**
 * Renders a list of games that a contest contains.
 */
const GamesList = React.createClass({

  propTypes: {
    boxScores: React.PropTypes.array,
    teams: React.PropTypes.object,
  },


  getGameList(games) {
    const gameList = [];

    _forEach(games, (game) => {
      // do we have teams?
      if (this.props.teams.hasOwnProperty('teams')) {
        gameList.push(
          <tr key={game.pk}>
            <td className="teams">
              {this.props.teams.teams[game.fields.away_id].alias}&nbsp;vs&nbsp;
              {this.props.teams.teams[game.fields.home_id].alias}
            </td>
            <td className="time">{moment(game.fields.created, moment.ISO_8601).format('h:mma')}</td>
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
