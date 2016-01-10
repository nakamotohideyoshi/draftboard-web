import React from 'react'

import * as AppActions from '../../stores/app-state-store'
import LivePMRProgressBar from './live-pmr-progress-bar'


/**
 * One entry within the live history ticker
 */
var LiveLineupPlayer = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    player: React.PropTypes.object.isRequired,
    onClick: React.PropTypes.func.isRequired
  },

  render: function() {
    const playStatusClass = 'live-lineup-player__play-status play-status--' + this.props.player.playStatus
    let stats = this.props.player.stats


    // TEMP
    let playerInitials = this.props.player.info.name.match(/\b(\w)/g).join('')

    if (stats === undefined) {
      stats = {pos: "", fp: 0}
    }

    let hoverStats = (
      <div className="live-lineup-player__hover-stats">
        <ul>
          <li>
            <div className="hover-stats__amount">{ stats.fp }</div>
            <div className="hover-stats__name">PTS</div>
          </li>
          <li>
            <div className="hover-stats__amount">2</div>
            <div className="hover-stats__name">RB</div>
          </li>
          <li>
            <div className="hover-stats__amount">0</div>
            <div className="hover-stats__name">ST</div>
          </li>
          <li>
            <div className="hover-stats__amount">6</div>
            <div className="hover-stats__name">ASST</div>
          </li>
          <li>
            <div className="hover-stats__amount">2</div>
            <div className="hover-stats__name">BLK</div>
          </li>
          <li>
            <div className="hover-stats__amount">2</div>
            <div className="hover-stats__name">TO</div>
          </li>
        </ul>
      </div>
    )

    let className = 'live-lineup-player'
    if (stats.decimalRemaining === 0.01) {
      className += ' state--not-playing'
    } else {
      className += ' state--is-playing'
    }

    // for now flip the order of DOM elements, find a better fix in the future
    if (this.props.whichSide === 'opponent') {
      return (
        <li className={className} onClick={this.props.onClick}>
          { hoverStats }
          <div className={ playStatusClass }></div>
          <div className="live-lineup-player__points">{stats.fp}</div>
          <div className="live-lineup-player__status"></div>
          <div className="live-lineup-player__photo">
            <LivePMRProgressBar decimalRemaining={stats.decimalRemaining} strokeWidth="2" backgroundHex="46495e" hexStart="e33c3c" hexEnd="871c5a" svgWidth="50" />
            <div className="live-lineup-player__initials">{playerInitials}</div>
          </div>
          <div className="live-lineup-player__position">{this.props.player.info.position}</div>
        </li>
      )
    }

    return (
      <li className={className} onClick={this.props.onClick}>
        <div className="live-lineup-player__position">{this.props.player.info.position}</div>
        <div className="live-lineup-player__photo">
          <LivePMRProgressBar decimalRemaining={stats.decimalRemaining} strokeWidth="2" backgroundHex="46495e" hexStart="34B4CC" hexEnd="2871AC" svgWidth="50" />
          <div className="live-lineup-player__initials">{playerInitials}</div>
        </div>
        <div className="live-lineup-player__status"></div>
        <div className="live-lineup-player__points">{stats.fp}</div>
        <div className={ playStatusClass }></div>
        { hoverStats }
      </li>
    )


  }
})


module.exports = LiveLineupPlayer
