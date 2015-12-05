import React from 'react'

import LiveLineupPlayer from './live-lineup-player'


/**
 * The history ticker at the bottom of the live page
 */
var LiveLineup = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    lineup: React.PropTypes.object.isRequired
  },

  render() {
    const self = this
    const draftGroup = self.props.lineup.draftGroup
    const currentPlayers = self.props.lineup.roster.map(function(playerId) {
      const player = {
        info: draftGroup.playersInfo[playerId],
        stats: draftGroup.playersStats[playerId]
      }

      return (
        <LiveLineupPlayer key={playerId} player={ player } whichSide = { self.props.whichSide } />
      )
    })

    const className = 'cmp-live__lineup live-lineup live-lineup--' + self.props.whichSide

    return (
      <div className={ className }>
        <ul className="live-lineup__players">
          {currentPlayers}
        </ul>

        <div className="view-player-detail"  />
      </div>
    )
  }
})


module.exports = LiveLineup
