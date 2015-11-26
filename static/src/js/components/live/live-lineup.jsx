import React from 'react'
import renderComponent from '../../lib/render-component'

import * as AppActions from '../../stores/app-state-store'
import LiveLineupPlayer from './live-lineup-player'


/**
 * The history ticker at the bottom of the live page
 */
var LiveLineup = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired
  },

  getDefaultProps: function() {
    return {
      whichSide: ''
    }
  },

  viewPlayerDetails: function() {
    AppActions.toggleLiveRightPane('appstate--live-player-pane--open')
  },

  render: function() {
    var lineupData

    // if (this.props.whichSide === 'me') {
    //   lineupData = LiveStore.data.myLineupPlayers
    // } else {
    //   lineupData = LiveStore.data.opponentLineupPlayers
    // }

    // var currentPlayers = lineupData.order.map(function(playerId) {
    //   // need a better check here
    //   if (lineupData.players[playerId] === undefined) {
    //     return null
    //   }

    //   return (
    //     <LiveLineupPlayer key={playerId} player={lineupData.players[playerId]} />
    //   )
    // })

    var className = 'cmp-live__lineup live-lineup live-lineup--' + this.props.whichSide

    // {currentPlayers}
    return (
      <div className={ className }>
        <ul className="live-lineup__players">
        </ul>

        <div className="view-player-detail" onClick={this.viewPlayerDetails} />
      </div>
    )
  }
})


// Render the component.
renderComponent(<LiveLineup />, '.live-lineup')

module.exports = LiveLineup
