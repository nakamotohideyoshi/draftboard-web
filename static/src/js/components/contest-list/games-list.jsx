import React from 'react'
import {forEach as _forEach} from 'lodash'
import moment from 'moment'


var GamesList = React.createClass({

  propTypes: {
    boxScores: React.PropTypes.array,
    teams: React.PropTypes.object
  },


  getGameList: function(games) {
    let gameList = []

    _forEach(games, function(game) {
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
        )
      }
    }.bind(this))

    return gameList
  },


  render: function() {

    if (!this.props.boxScores) {
      return (
        <div>Loading...</div>
      )
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
    )
  }

})


module.exports = GamesList
