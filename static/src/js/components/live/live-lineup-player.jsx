import React from 'react'

import * as AppActions from '../../stores/app-state-store'
import LivePMRProgressBar from './live-pmr-progress-bar'


/**
 * One entry within the live history ticker
 */
var LiveLineupPlayer = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    player: React.PropTypes.object.isRequired
  },

  viewPlayerDetails() {
    AppActions.toggleLiveRightPane('appstate--live-player-pane--open')
  },

  render: function() {
    const playStatusClass = 'live-lineup-player__play-status play-status--' + this.props.player.playStatus
    let stats = this.props.player.stats

    if (stats === undefined) {
      stats = {pos: "", fp: 0}
    }

    // for now flip the order of DOM elements, find a better fix in the future
    if (this.props.whichSide === 'opponent') {
      return (
        <li className="live-lineup-player state--is-playing" onClick={ this.viewPlayerDetails }>
          <div className={ playStatusClass }></div>
          <div className="live-lineup-player__points">{stats.fp}</div>
          <div className="live-lineup-player__status"></div>
          <div className="live-lineup-player__photo">
            <LivePMRProgressBar decimalRemaining="0.3" strokeWidth="2" backgroundHex="46495e" hexStart="e33c3c" hexEnd="871c5a" svgWidth="50" />
          </div>
          <div className="live-lineup-player__position">{this.props.player.info.position}</div>
        </li>
      )
    }

    return (
      <li className="live-lineup-player state--is-playing" onClick={ this.viewPlayerDetails }>
        <div className="live-lineup-player__position">{this.props.player.info.position}</div>
        <div className="live-lineup-player__photo">
          <LivePMRProgressBar decimalRemaining="0.3" strokeWidth="2" backgroundHex="46495e" hexStart="34B4CC" hexEnd="2871AC" svgWidth="50" />
        </div>
        <div className="live-lineup-player__status"></div>
        <div className="live-lineup-player__points">{stats.fp}</div>
        <div className={ playStatusClass }></div>
      </li>
    )


  }
})


module.exports = LiveLineupPlayer
