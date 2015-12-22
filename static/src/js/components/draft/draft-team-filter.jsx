import React from 'react'
// import ReactDom  from 'react-dom'
import moment from 'moment'
import {forEach as _forEach} from 'lodash'



/**
 * A list of games & participating teams, each with a checkboxe that act as filters for the player
 * list.
 */
const DraftTeamFilter = React.createClass({
  filterTitle: 'teamFilter',

  propTypes: {
    games: React.PropTypes.array.isRequired,
    isVisible: React.PropTypes.bool.isRequired,
    onFilterChange: React.PropTypes.func.isRequired,
    selectedTeams: React.PropTypes.array.isRequired
  },


  getDefaultProps: function() {
    return {
      isVisible: false
    }
  },


  collectSelectedTeams: function() {
    let checkedBoxes = this.refs['games-list'].querySelectorAll('input[type="checkbox"]:checked')
    let games = []
    _forEach(checkedBoxes, function(input) {
      games.push(input.value)
    })
    return games
  },


  checkAllTeams: function(checkboxes) {
    _forEach(checkboxes, function(input) {
      input.checked=true
    })
  },


  unCheckAllTeams: function(checkboxes) {
    _forEach(checkboxes, function(input) {
      input.checked=false
    })
  },


  handleGameClick: function(game, e) {
    // stopPropagation() doesn't work so we need to manually ignore team clicks.
    if (e.target.tagName === 'LABEL' || e.target.tagName === 'INPUT') {
      return
    }

    let gameNode = this.refs['game-' + game.pk]
    let checkboxes = gameNode.querySelectorAll('input[type="checkbox"]')
    let allChecked = true

    _forEach(checkboxes, function(input) {
      if (!input.checked) {
        allChecked = false;
        return
      }
    })

    if (allChecked) {
      this.unCheckAllTeams(checkboxes)
    } else {
      this.checkAllTeams(checkboxes)
    }

    this.handleTeamOnChange()
  },


  handleTeamOnChange: function(e) {
    this.props.onFilterChange(this.filterTitle, 'team_srid', this.collectSelectedTeams())
  },


  handleTeamClick: function(team, e) {
    // Like noted above, this doesn't work in react.
    // https://github.com/facebook/react/issues/1691
    e.stopPropagation()

    this.handleTeamOnChange()
  },


  isTeamSelected: function(teamId) {
    return this.props.selectedTeams.indexOf(teamId) !== -1
  },


  getGames: function() {
    return this.props.games.map(function(game) {
      return ([
        <div
          className="game scroll-item"
          key={game.pk}
          onClick={this.handleGameClick.bind(this, game)}
          ref={'game-' + game.pk}
        >
          <div className="left">
            <div className="team away">
              <input
                type="checkbox"
                id={game.pk + "-" + game.fields.away_id}
                value={game.fields.srid_away}
                onChange={this.handleTeamClick.bind(this, game.fields.srid_away)}
                />
              <label
                htmlFor={game.pk + "-" + game.fields.away_id}

              >{game.fields.away_id}</label>
            </div>

            <div className="team home">
              <input
                type="checkbox"
                id={game.pk + "-" + game.fields.home_id}
                value={game.fields.srid_home}
                onChange={this.handleTeamClick.bind(this, game.fields.srid_home)}
                />
              <label
                htmlFor={game.pk + "-" + game.fields.home_id}

              >{game.fields.home_id}</label>
            </div>
          </div>

          <div className="right">
            <div className="start_time">
              {moment(game.fields.created, moment.ISO_8601).format('h:mma')}
            </div>
          </div>
        </div>,
        <div className="separator half"></div>
      ])
    }.bind(this))
  },


  render: function() {
    return (
      <div className="cmp-draft-team-filter">
        <div className="slider-content">
          <div className="slider-content-holder">
            <div className="games-list" ref="games-list">
              <div
                className="game scroll-item"
              >
                All Games
              </div>
              {this.getGames()}
            </div>
          </div>
        </div>
      </div>
    )
  }

})


module.exports = DraftTeamFilter
