import React from 'react'
// import ReactDom  from 'react-dom'
import moment from 'moment'
import {forEach as _forEach} from 'lodash'
import classNames from 'classnames'


/**
 * A list of games & participating teams, each with a checkboxe that act as filters for the player
 * list.
 */
const DraftTeamFilter = React.createClass({
  filterTitle: 'teamFilter',

  propTypes: {
    boxScores: React.PropTypes.array.isRequired,
    games: React.PropTypes.array.isRequired,
    isVisible: React.PropTypes.bool.isRequired,
    onFilterChange: React.PropTypes.func.isRequired,
    selectedTeams: React.PropTypes.array.isRequired,
    teams: React.PropTypes.object.isRequired,
    sport: React.PropTypes.string
  },


  getDefaultProps: function() {
    return {
      isVisible: false
    }
  },


  /**
   * Scrolls slider left.
   */
  handleScrollLeft() {
    const content = this.refs.content;
    let left = parseInt(content.style.left) | 0
    this.refs.content.style.left = (left + 400) + 'px';
  },


  /**
   * Scrolls slider right.
   */
  handleScrollRight() {
    const content = this.refs.content;
    let left = parseInt(content.style.left, 10) | 0
    content.style.left = (left - 400) + 'px';
  },


  getAllTeams: function() {
    let allTeams = []

    _forEach(this.props.games, function(game) {
      allTeams.push(game.srid_home)
      allTeams.push(game.srid_away)
    })

    return allTeams
  },


  selectAllTeams: function(checkboxes) {
    this.handleTeamsChange(this.getAllTeams())
  },


  unselectAllTeams: function(checkboxes) {
    this.handleTeamsChange([])
  },


  isTeamSelected: function(selectedTeams, teamId) {
    return selectedTeams.indexOf(teamId) !== -1
  },


  removeTeamFromList(list, team) {
    if (list.indexOf(team) !== -1) {
      list.splice(list.indexOf(team), 1)
    }
  },


  handleGameClick: function(game, e) {
    let newTeams = this.props.selectedTeams.slice()

    if (this.isTeamSelected(newTeams, game.srid_home) && this.isTeamSelected(newTeams, game.srid_away)) {
      this.removeTeamFromList(newTeams, game.srid_home)
      this.removeTeamFromList(newTeams, game.srid_away)
    } else {
      this.removeTeamFromList(newTeams, game.srid_home)
      this.removeTeamFromList(newTeams, game.srid_away)
      newTeams.push(game.srid_home)
      newTeams.push(game.srid_away)
    }

    this.handleTeamsChange(newTeams)
  },


  handleTeamsChange: function(selectedTeams) {
    this.props.onFilterChange(this.filterTitle, 'team_srid', selectedTeams)
  },


  handleAllClick: function() {
    if (this.getAllTeams().length > this.props.selectedTeams.length) {
      this.selectAllTeams()
    } else {
      this.unselectAllTeams()
    }
  },


  handleTeamClick: function(teamId, e) {
    e.stopPropagation()
    let newTeams = this.props.selectedTeams.slice()

    if (this.isTeamSelected(newTeams, teamId)) {
      this.removeTeamFromList(newTeams, teamId)
    } else {
      newTeams.push(teamId)
    }
    this.handleTeamsChange(newTeams)
  },


  // Safely get the team alias. Oh lord don't hate me.
  getTeamAlias: function(teamSrid) {
    if (this.props.teams.hasOwnProperty(this.props.sport)) {
      if (this.props.teams[this.props.sport].hasOwnProperty('teams')) {
        if (this.props.teams[this.props.sport].teams.hasOwnProperty(teamSrid)) {
          return this.props.teams[this.props.sport].teams[teamSrid].alias
        }
      }
    }

    return ''
  },


  getGames: function() {
    return this.props.games.map(function(game) {
      let homeClasses = classNames('team home', { 'selected': this.isTeamSelected(this.props.selectedTeams, game.srid_home) })
      let awayClasses = classNames('team away', { 'selected': this.isTeamSelected(this.props.selectedTeams, game.srid_away) })

      return ([
        <div
          className="game scroll-item"
          key={game.pk}
          onClick={this.handleGameClick.bind(this, game)}
          ref={'game-' + game.pk}
        >
          <div className="left">
            <div className={awayClasses} onClick={this.handleTeamClick.bind(this, game.srid_away)}>
              <span
                className="teamName"
              >{this.getTeamAlias(game.srid_away)}</span>
            </div>

            <div className={homeClasses} onClick={this.handleTeamClick.bind(this, game.srid_home)}>
              <span
                className="teamName"
              >{this.getTeamAlias(game.srid_home)}</span>
            </div>
          </div>

          <div className="right">
            <div className="start_time">
              {moment(game.start, moment.ISO_8601).format('h:mma')}
            </div>
          </div>
        </div>,
        <div className="separator half"></div>
      ])
    }.bind(this))
  },


  render: function() {
    if (!this.props.isVisible) {
      return <div></div>
    }

    return (
      <div className="cmp-draft-team-filter">
        <div className="slider">

          <div className="arrow">
            <div className="left-arrow-icon" onClick={this.handleScrollLeft}></div>
          </div>

          <div className="slider-content">
            <div className="slider-content-holder" ref="content">
              <div className="games-list" ref="games-list">
                <div
                  className="game scroll-item allTeams"
                  onClick={this.handleAllClick}
                  >
                  <span
                    className="teamName"
                    >All Games</span>
                </div>
                <div className="separator half"></div>
                {this.getGames()}
              </div>
            </div>
          </div>

          <div className="arrow right">
            <div className="right-arrow-icon" onClick={this.handleScrollRight}></div>
          </div>

        </div>
      </div>
    )
  }

})


module.exports = DraftTeamFilter
