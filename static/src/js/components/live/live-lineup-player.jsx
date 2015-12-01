import React from 'react'

import * as AppActions from '../../stores/app-state-store'
import LivePMRProgressBar from './live-pmr-progress-bar'


/**
 * One entry within the live history ticker
 */
var LiveLineupPlayer = React.createClass({
  propTypes: {
    player: React.PropTypes.object.isRequired
  },

  viewPlayerDetails() {
    AppActions.toggleLiveRightPane('appstate--live-player-pane--open')
  },

  render: function() {
    var playStatusClass = 'live-lineup-player__play-status play-status--' + this.props.player.playStatus

    return (
      <li className="live-lineup-player state--is-playing" onClick={ this.viewPlayerDetails }>
        <div className="live-lineup-player__position">{this.props.player.info.position}</div>
        <div className="live-lineup-player__photo">
          <LivePMRProgressBar decimalRemaining="0.3" strokeWidth="2" backgroundHex="46495e" hexStart="34B4CC" hexEnd="2871AC" svgWidth="50" />
        </div>
        <div className="live-lineup-player__status"></div>
        <div className="live-lineup-player__points">{this.props.player.stats.fp}</div>
        <div className={ playStatusClass }></div>
      </li>
    )
  }
})


module.exports = LiveLineupPlayer
