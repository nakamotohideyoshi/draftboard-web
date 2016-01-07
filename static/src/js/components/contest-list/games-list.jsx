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
      gameList.push(
        <li key={game.pk}>
          <span className="teams">
            {this.props.teams.teams[game.fields.away_id].alias}&nbsp;vs&nbsp;
            {this.props.teams.teams[game.fields.home_id].alias}
          </span>
          <span className="time">{moment(game.fields.created, moment.ISO_8601).format('h:mma')}</span>
        </li>
      )
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

        <h6 className="header">
          <span className="place">Teams</span>
          <span className="prize">Time</span>
        </h6>

        <ul>
          {this.getGameList(this.props.boxScores)}
        </ul>
      </div>
    )
  }

})


module.exports = GamesList
