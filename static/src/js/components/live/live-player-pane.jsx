import React from 'react'
import _ from 'lodash'

import * as AppActions from '../../stores/app-state-store'
import LivePMRProgressBar from './live-pmr-progress-bar'
import log from '../../lib/logging'

import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import store from '../../store'



/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
const LivePlayerPane = React.createClass({

  propTypes: {
    eventHistory: React.PropTypes.array.isRequired,
    player: React.PropTypes.object.isRequired,
    whichSide: React.PropTypes.string.isRequired,
    game: React.PropTypes.object
  },

  closePane: function() {
    log.debug('LivePlayerPane.closePane()')

    this.props.whichSide === 'opponent' ? AppActions.togglePlayerPane('right') : AppActions.togglePlayerPane('left')
  },

  renderStatsAverage: function() {
    const player = this.props.player

    if (player.hasOwnProperty('seasonalStats') === false) {
      return (
        <div className='player-stats'>
          <ul />
        </div>
      )
    }

    const stats = player.seasonalStats

    return (
      <div className='player-stats'>
        <ul>
          <li>
            <div className='stat-name'>FPPG</div>
            <div className='stat-score'>{ stats.avg_fp.toFixed(1) }</div>
          </li>
          <li>
            <div className='stat-name'>PPG</div>
            <div className='stat-score'>{ stats.avg_points.toFixed(1) }</div>
          </li>
          <li>
            <div className='stat-name'>RPG</div>
            <div className='stat-score'>{ stats.avg_rebounds.toFixed(1) }</div>
          </li>
          <li>
            <div className='stat-name'>APG</div>
            <div className='stat-score'>{ stats.avg_assists.toFixed(1) }</div>
          </li>
          <li>
            <div className='stat-name'>STLPG</div>
            <div className='stat-score'>{ stats.avg_steals.toFixed(1) }</div>
          </li>
          <li>
            <div className='stat-name'>TOPG</div>
            <div className='stat-score'>{ stats.avg_turnovers.toFixed(1) }</div>
          </li>
        </ul>
      </div>
    )
  },

  renderCurrentGame: function() {
    log.debug('LivePlayerPane.renderCurrentGame')
    const player = this.props.player
    const game = this.props.game

    // if the game isn't loaded yet or something
    if (!game.hasOwnProperty('boxscore')) {
      log.debug('renderCurrentGame() - boxScore undefined')
      return (<div className='current-game' />)
    }

    const boxScore = game.boxscore

    let clock
    if (boxScore.status === 'closed') {
      clock = (
        <div className='current-game__time'>
          <div className='current-game__time__timer' />
          <div className='current-game__time__period'>Final</div>
        </div>
      )
    } else {
      clock = (
        <div className='current-game__time'>
          <div className='current-game__time__timer'>{ boxScore.clock }</div>
          <div className='current-game__time__period'>{ boxScore.quarterDisplay }</div>
        </div>
      )
    }


    return (
      <div className='current-game'>
        <div>
          <div className='current-game__team1'>
            <div className='current-game__team1__points'>{ boxScore.home_score }</div>
            <div className='current-game__team-name'>
              <div className='city'>{ game.homeTeamInfo.city }</div>
              <div className='name'>{ game.homeTeamInfo.name }</div>
            </div>
          </div>
          { clock }
          <div className='current-game__team2'>
            <div className='current-game__team1__points'>{ boxScore.away_score }</div>
            <div className='current-game__team-name'>
              <div className='city'>{ game.awayTeamInfo.city }</div>
              <div className='name'>{ game.awayTeamInfo.name }</div>
            </div>
          </div>
        </div>
      </div>
    )
  },

  renderActivities: function() {
    let index = 0
    const eventHistory = this.props.eventHistory.reverse()

    let activitiesHTML = eventHistory.map((activity) => {
      index += 1
      const { points, info, when } = activity
      return (
        <li className='activity' key={index}>
          <div className='points-gained'>{points}</div>
          <div className='activity-info'>
            {info}
            <p className='time'>{when}</p>
          </div>
        </li>
      )
    })

    return (
      <div className='recent-activity'>
        <div className='recent-activity__title'>Recent activity</div>
        <ul>{ activitiesHTML }</ul>
      </div>
    )
  },

  renderHeader: function() {
    const player = this.props.player
    const game = this.props.game
    const teamInfo = player.teamInfo

    let percentageTimeRemaining = 1
    let fp = 0

    // if the game has not started
    if (game !== undefined) {
      percentageTimeRemaining = game.timeRemaining / 48
    }

    if (player.stats !== undefined) {
      fp = player.stats.fp
    }


    return (
      <section className='header-section'>
        <div className="header__player-image" />

        <div className='header__team-role'>
          { teamInfo.city } { teamInfo.name } - { player.info.position }
        </div>
        <div className='header__name'>{ player.info.name }</div>

        <div className='header__pts-stats'>
          <div className="header__pts-stats__info">
            <LivePMRProgressBar
              decimalRemaining={ player.stats.decimalRemaining }
              strokeWidth="1"
              backgroundHex="46495e"
              hexStart="34B4CC"
              hexEnd="2871AC"
              svgWidth="50"
            />

            <div className="header__pts-stats__info__insvg">
              <p>pts</p>
              <p>{ fp }</p>
            </div>
          </div>

          <div className="header__pts-stats__info">
            <p>% owned</p>
            <p>18</p>
          </div>

        </div>
      </section>
    )
  },

  render: function() {
    const side = this.props.whichSide === 'opponent' ? 'right' : 'left'
    let classNames = 'player-detail-pane live-player-pane live-pane live-pane--' + side + ' live-pane-player--' + side

    const teamSRID = this.props.player.info.team_srid
    const game = this.props.game

    return (
      <div className={classNames}>
        <div className="live-pane__close" onClick={this.closePane}></div>

        <div className="pane-upper">
          { this.renderHeader() }
          { this.renderStatsAverage() }
          { this.renderCurrentGame() }
        </div>

        <div className="pane-lower">
          { this.renderActivities() }
        </div>
      </div>
    )
  }
})


export default LivePlayerPane
