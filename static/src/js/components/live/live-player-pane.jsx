import React from 'react'

import * as AppActions from '../../stores/app-state-store'
import LivePMRProgressBar from './live-pmr-progress-bar'

import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import store from '../../store'



/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
const LivePlayerPane = React.createClass({

  propTypes: {
    player: React.PropTypes.object.isRequired,
    whichSide: React.PropTypes.string.isRequired,
    boxScore: React.PropTypes.object
  },

  closePane: function() {
    console.log('LivePlayerPane.closePane()')
    this.props.whichSide === 'opponent' ? AppActions.closePlayerPane('right') : AppActions.closePlayerPane('left')
  },

  renderStatsAverage: function() {
    const player = this.props.player
    let fp = 0

    if (player.stats !== undefined) {
      fp = player.stats.fp
    }

    return (
      <div className='live-player-pane__player-stats'>
        <ul>
          <li>
            <div className='stat-name'>{ player.info.name }</div>
            <div className='stat-score'>{ fp }</div>
          </li>
        </ul>
      </div>
    )
  },

  renderCurrentGame: function() {
    const player = this.props.player
    const boxScore = this.props.boxScore

    if (boxScore === undefined) {
      return (<div className='live-player-pane__current-game' />)
    }

    return (
      <div className='live-player-pane__current-game'>
        <div>
          <div className='live-player-pane__current-game__team1'>
            <div className='live-player-pane__current-game__team1__points'>{ boxScore.fields.home_score }</div>
            <div><img src="" className='live-player-pane__current-game__team-logo' /></div>
          </div>
          <div className='live-player-pane__current-game__time'>
            <div className='live-player-pane__current-game__time__timer'>{ boxScore.fields.clock }</div>
            <div className='live-player-pane__current-game__time__period'>{ boxScore.fields.quarter } quarter</div>
          </div>
          <div className='live-player-pane__current-game__team2'>
            <div className='live-player-pane__current-game__team1__points'>{ boxScore.fields.away_score }</div>
            <img src="" className='live-player-pane__current-game__team-logo' />
          </div>
        </div>
      </div>
    )
  },

  renderActivities: function() {
    const activities = [
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      },
      {
        'description': "Lebron James assists Russel Westbrook's 3-pointer",
        'points': '+2',
        'time': '4:13 - 4th'
      }
    ]

    let index = 0
    let activitiesHTML = activities.map((activity) => {
      index += 1
      const { points, description, time } = activity
      return (
        <li className='activity' key={index}>
          <div className='points-gained'>{points}</div>
          <div className='activity-info'>
            {description}
            <p className='time'>{time}</p>
          </div>
        </li>
      )
    })

    return (
      <div className='live-player-pane__recent-activity'>
        <div className='live-player-pane__recent-activity__title'>Recent activity</div>
        <ul>{ activitiesHTML }</ul>
      </div>
    )
  },

  renderHeader: function() {
    const player = this.props.player
    const boxScore = this.props.boxScore
    let percentageTimeRemaining = 1
    let fp = 0

    // if the game has not started
    if (boxScore !== undefined) {
      percentageTimeRemaining = boxScore.fields.timeRemaining / 48
    }

    if (player.stats !== undefined) {
      fp = player.stats.fp
    }


    return (
      <div className='live-player-pane__header'>
        <div className='live-player-pane__header__team-role'>{ player.info.position }</div>
        <div className='live-player-pane__header__name'>{ player.info.name }</div>

        <div className='live-player-pane__header__pts-stats'>
            <div className="live-player-pane__header__pts-stats__info">
            <LivePMRProgressBar
              decimalRemaining="0.3"
              strokeWidth="2"
              backgroundHex="46495e"
              hexStart="e33c3c"
              hexEnd="871c5a"
              svgWidth="50" />

              <div className="live-player-pane__header__pts-stats__info__insvg">
                <p>pts</p>
                <p>{ fp }</p>
              </div>
            </div>

            <div className="live-player-pane__header__pts-stats__info">
              <p>% owned</p>
              <p>18</p>
            </div>

            <img className="live-player-pane__header__player-image" src="" />
        </div>
      </div>
    )
  },

  render: function() {
    const side = this.props.whichSide === 'opponent' ? 'right' : 'left'
    let classNames = 'live-pane live-pane--' + side + ' live-pane-player--' + side

    return (
      <div className={classNames}>
        <div className="live-pane__close" onClick={this.closePane}></div>
        <div className="live-player-pane">
        { this.renderHeader() }
        { this.renderStatsAverage() }
        { this.renderCurrentGame() }
        { this.renderActivities() }
        </div>
      </div>
    )
  }
})


export default LivePlayerPane
