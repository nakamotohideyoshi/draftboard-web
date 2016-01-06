import React from 'react'

import * as AppActions from '../../stores/app-state-store'
import LiveLineupPlayer from './live-lineup-player'
import LivePlayerPane from './live-player-pane'
import log from '../../lib/logging'


/**
 * The history ticker at the bottom of the live page
 */
var LiveLineup = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    lineup: React.PropTypes.object.isRequired,
    currentBoxScores: React.PropTypes.object.isRequired
  },

  getInitialState() {
    return {
      // When true, render and show the detail pane
      viewPlayerDetails: undefined
    }
  },


  togglePlayerDetail(playerId) {
    log.debug('togglePlayerDetail()', playerId)
    if (this.state.viewPlayerDetails === playerId) {
      log.debug('togglePlayerDetail() - close')
      this.setState({viewPlayerDetails: undefined})
      this.props.whichSide === 'opponent' ? AppActions.closePlayerPane('right') : AppActions.closePlayerPane('left')
    } else {
      log.debug('togglePlayerDetail() - open')
      this.setState({viewPlayerDetails: playerId})
      this.props.whichSide === 'opponent' ? AppActions.openPlayerPane('right') : AppActions.openPlayerPane('left')
    }
  },


  render() {
    const self = this
    const draftGroup = self.props.lineup.draftGroup
    const currentPlayers = self.props.lineup.roster.map(function(playerId) {
      const player = self.props.lineup.rosterDetails[playerId]
      const boxScore = self.props.currentBoxScores[player.info.game_srid]

      return (
        <LiveLineupPlayer key={playerId} player={player} whichSide={self.props.whichSide} onClick={self.togglePlayerDetail.bind(self, playerId)} />
      )
    })

    let playerPane
    if (self.state.viewPlayerDetails) {
      const player = self.props.lineup.rosterDetails[self.state.viewPlayerDetails]
      const boxScore = self.props.currentBoxScores[player.info.game_srid]

      playerPane = (
        <LivePlayerPane whichSide={self.props.whichSide} player={player} boxScore={boxScore} />
      )
    }


    const className = 'cmp-live__lineup live-lineup live-lineup--' + self.props.whichSide

    return (
      <div className={ className }>
        <ul className="live-lineup__players">
          {currentPlayers}
        </ul>

        { playerPane }
        <div className="view-player-detail"  />
      </div>
    )
  }
})


module.exports = LiveLineup
