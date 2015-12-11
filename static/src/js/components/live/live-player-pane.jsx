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
    player: React.PropTypes.object,
    side: React.PropTypes.string
  },

  closePane: function() {
    AppActions.closePlayerPane(this.props.side)
  },

  renderStatsAverage: function() {
    const { stats } = this.props.player
    let statsHTML = stats.map((stats) => {
      const { name, score } = stats
      return (
        <li>
          <div className='stat-name'>{ name }</div>
          <div className='stat-score'>{ score }</div>
        </li>
      )
    })

    return (
      <div className='live-player-pane__player-stats'>
        <ul>{ statsHTML }</ul>
      </div>
    )
  },

  renderCurrentGame: function() {
    const { game } = this.props.player

    return (
      <div className='live-player-pane__current-game'>
        <div>
          <div className='live-player-pane__current-game__team1'>
            <div className='live-player-pane__current-game__team1__points'>{ game.teamA.points }</div>
            <div><img src={ game.teamA.logo } className='live-player-pane__current-game__team-logo' /></div>
          </div>
          <div className='live-player-pane__current-game__time'>
            <div className='live-player-pane__current-game__time__timer'>{ game.time }</div>
            <div className='live-player-pane__current-game__time__period'>{ game.part }</div>
          </div>
          <div className='live-player-pane__current-game__team2'>
            <div className='live-player-pane__current-game__team1__points'>{ game.teamB.points }</div>
            <img src={ game.teamB.logo } className='live-player-pane__current-game__team-logo' />
          </div>
        </div>
      </div>
    )
  },

  renderActivities: function() {
    const { activities } = this.props.player
    let activitiesHTML = activities.map((activity) => {
      const { points, description, time } = activity
      return (
        <li className='activity'>
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
    const { name, position, pts, owned, img } = this.props.player
    return (
      <div className='live-player-pane__header'>
        <div className='live-player-pane__header__team-role'>{ position }</div>
        <div className='live-player-pane__header__name'>{ name }</div>

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
                <p>{ pts }</p>
              </div>
            </div>

            <div className="live-player-pane__header__pts-stats__info">
              <p>% owned</p>
              <p>{ owned }</p>
            </div>

            <img className="live-player-pane__header__player-image" src={ img } />
        </div>
      </div>
    )
  },

  render: function() {
    let classNames = 'live-pane live-pane--' + this.props.side + ' live-pane-player--' + this.props.side

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
