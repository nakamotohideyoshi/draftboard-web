import React from 'react'

import * as AppActions from '../../stores/app-state-store'
import LivePMRProgressBar from './live-pmr-progress-bar'
import log from '../../lib/logging'


/**
 * When a lineup player is clicked, this pane will show seasonal data, player information, team information and
 * game history.
 */
const LivePlayerPane = React.createClass({

  propTypes: {
    eventHistory: React.PropTypes.array.isRequired,
    player: React.PropTypes.object.isRequired,
    whichSide: React.PropTypes.string.isRequired,
    game: React.PropTypes.object,
  },

  /**
   * Close the player pane using AppActions
   */
  closePane() {
    log.debug('LivePlayerPane.closePane()')

    if (this.props.whichSide === 'opponent') {
      AppActions.togglePlayerPane('right')
    } else {
      AppActions.togglePlayerPane('left')
    }
  },

  /**
   * Render out the seasonal stats
   *
   * @return {JSXElement}
   */
  renderStatsAverage() {
    const player = this.props.player

    let renderedStats
    if (player.hasOwnProperty('seasonalStats') === true) {
      // ordered stats
      const statTypes = ['fp', 'points', 'rebounds', 'assists', 'steals', 'turnovers']
      const statNames = ['FPPG', 'PPG', 'RPG', 'APG', 'stlpg', 'TOPG']

      renderedStats = statTypes.map((statType, index) => {
        const value = player.seasonalStats[`avg_${statType}`].toFixed(1)

        return (
          <li key={statType}>
            <div className="stat-name">{statNames[index]}</div>
            <div className="stat-score">{value}</div>
          </li>
        )
      })
    }

    return (
      <div className="player-stats">
        <ul>
          {renderedStats}
        </ul>
      </div>
    )
  },

  /**
   * Render out information about the player's current game
   *
   * @return {JSXElement}
   */
  renderCurrentGame() {
    const game = this.props.game

    // if the game isn't loaded yet or something then return
    if (!game.hasOwnProperty('boxscore')) {
      log.debug('LivePlayerPane.renderCurrentGame() - boxScore undefined')
      return (<div className="current-game" />)
    }

    const boxScore = game.boxscore

    // TODO Live - make sure clock and quarter display are set in liveSelector so we don't do logic in the component
    let gameTimeInfo
    if (boxScore.status === 'closed') {
      gameTimeInfo = ['', 'Final']
    } else {
      gameTimeInfo = [
        boxScore.clock,
        boxScore.quarterDisplay,
      ]
    }

    return (
      <div className="current-game">
        <div>
          <div className="current-game__team1">
            <div className="current-game__team1__points">{boxScore.home_score}</div>
            <div className="current-game__team-name">
              <div className="city">{game.homeTeamInfo.city}</div>
              <div className="name">{game.homeTeamInfo.name}</div>
            </div>
          </div>
          <div className="current-game__time">
            <div className="current-game__time__timer">{gameTimeInfo[0]}</div>
            <div className="current-game__time__period">{gameTimeInfo[1]}</div>
          </div>
          <div className="current-game__team2">
            <div className="current-game__team1__points">{boxScore.away_score}</div>
            <div className="current-game__team-name">
              <div className="city">{game.awayTeamInfo.city}</div>
              <div className="name">{game.awayTeamInfo.name}</div>
            </div>
          </div>
        </div>
      </div>
    )
  },

  /**
   * Render out the recent activities, aka props.eventHistory that's available
   * This history erases on refresh, is not cached and lives in the Live component state.
   *
   * @return {JSXElement}
   */
  renderActivities() {
    // reverse to show most recent event first
    const eventHistory = this.props.eventHistory

    const activitiesHTML = eventHistory.map((activity, index) => {
      const { points, info, when } = activity
      return (
        <li className="activity" key={index}>
          <div className="points-gained">{points}</div>
          <div className="activity-info">
            {info}
            <p className="time">{when}</p>
          </div>
        </li>
      )
    })

    return (
      <div className="recent-activity">
        <div className="recent-activity__title">Recent activity</div>
        <ul>{activitiesHTML}</ul>
      </div>
    )
  },

  /**
   * Render out the header of the pane, which includes team information and pertinent player information
   *
   * @return {JSXElement}
   */
  renderHeader() {
    const player = this.props.player
    const teamInfo = player.teamInfo

    let fp = 0

    // TODO Live - make sure this stat is in the liveSelector and remove logic from component
    if (player.stats !== undefined) {
      fp = player.stats.fp
    }

    return (
      <section className="header-section">
        <div className="header__player-image" />

        <div className="header__team-role">
          {teamInfo.city} {teamInfo.name} - {player.info.position}
        </div>
        <div className="header__name">{player.info.name}</div>

        <div className="header__pts-stats">
          <div className="header__pts-stats__info">
            <LivePMRProgressBar
              decimalRemaining={player.stats.decimalRemaining}
              strokeWidth={1}
              backgroundHex="46495e"
              hexStart="34B4CC"
              hexEnd="2871AC"
              svgWidth={50}
            />

            <div className="header__pts-stats__info__insvg">
              <p>pts</p>
              <p>{fp}</p>
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

  render() {
    const side = this.props.whichSide === 'opponent' ? 'right' : 'left'
    const className = `player-detail-pane live-player-pane live-pane live-pane--${side} live-pane-player--${side}`

    return (
      <div className={className}>
        <div className="live-pane__close" onClick={this.closePane}></div>

        <div className="pane-upper">
          {this.renderHeader()}
          {this.renderStatsAverage()}
          {this.renderCurrentGame()}
        </div>

        <div className="pane-lower">
          {this.renderActivities()}
        </div>
      </div>
    )
  },
})


export default LivePlayerPane
