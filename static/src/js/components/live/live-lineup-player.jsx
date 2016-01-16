import React from 'react'

import * as AppActions from '../../stores/app-state-store'
import LivePMRProgressBar from './live-pmr-progress-bar'
var ReactCSSTransitionGroup = require('react-addons-css-transition-group');

/**
 * One entry within the live history ticker
 */
var LiveLineupPlayer = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    player: React.PropTypes.object.isRequired,
    playersPlaying: React.PropTypes.array.isRequired,
    eventDescriptions: React.PropTypes.object.isRequired,
    onClick: React.PropTypes.func.isRequired
  },

  render: function() {
    let playStatusClass = 'live-lineup-player__play-status'
    const playerSRID = this.props.player.info.player_srid

    // if player is on the court, show
    if (this.props.playersPlaying.indexOf(playerSRID) !== -1) {
      playStatusClass += ' play-status--playing'
    }

    // if player makes fp, show why
    let eventDescription
    if (playerSRID in this.props.eventDescriptions) {
      const eventInfo = this.props.eventDescriptions[playerSRID]

      eventDescription = (
        <div className="live-lineup-player__event-description event-description showing">
          <div className="event-description__points">{ eventInfo.points }</div>
          <div className="event-description__info">{ eventInfo.info }</div>
          <div className="event-description__when">{ eventInfo.when }</div>
        </div>
      )
    }

    // TEMP
    let playerInitials = this.props.player.info.name.match(/\b(\w)/g).join('')

    let stats = this.props.player.stats
    if (stats === undefined) {
      stats = {pos: "", fp: 0}
    }

    let hoverStats
    if (this.props.player.liveStats !== undefined) {
      const liveStats = this.props.player.liveStats

      hoverStats = (
        <div className="live-lineup-player__hover-stats">
          <ul>
            <li>
              <div className="hover-stats__amount">{ liveStats.points }</div>
              <div className="hover-stats__name">PTS</div>
            </li>
            <li>
              <div className="hover-stats__amount">{ liveStats.rebounds }</div>
              <div className="hover-stats__name">RB</div>
            </li>
            <li>
              <div className="hover-stats__amount">{ liveStats.steals }</div>
              <div className="hover-stats__name">ST</div>
            </li>
            <li>
              <div className="hover-stats__amount">{ liveStats.assists }</div>
              <div className="hover-stats__name">ASST</div>
            </li>
            <li>
              <div className="hover-stats__amount">{ liveStats.blocks }</div>
              <div className="hover-stats__name">BLK</div>
            </li>
            <li>
              <div className="hover-stats__amount">{ liveStats.turnovers }</div>
              <div className="hover-stats__name">TO</div>
            </li>
          </ul>
        </div>
      )
    }

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
          <ReactCSSTransitionGroup transitionName="event-description" transitionEnterTimeout={0} transitionLeaveTimeout={0}>
            { eventDescription }
          </ReactCSSTransitionGroup>
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
        <ReactCSSTransitionGroup transitionName="event-description" transitionEnterTimeout={0} transitionLeaveTimeout={0}>
          { eventDescription }
        </ReactCSSTransitionGroup>
        { hoverStats }
      </li>
    )


  }
})


module.exports = LiveLineupPlayer
