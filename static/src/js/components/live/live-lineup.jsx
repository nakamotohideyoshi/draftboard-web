import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import { updatePath } from 'redux-simple-router'
import { vsprintf } from 'sprintf-js'

import { updateLiveMode } from '../../actions/live'
import * as AppActions from '../../stores/app-state-store'
import LiveLineupPlayer from './live-lineup-player'
import LivePlayerPane from './live-player-pane'
import log from '../../lib/logging'
import store from '../../store'


/**
 * The history ticker at the bottom of the live page
 */
var LiveLineup = React.createClass({
  propTypes: {
    whichSide: React.PropTypes.string.isRequired,
    lineup: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object.isRequired,
    currentBoxScores: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },

  getInitialState() {
    return {
      // When true, render and show the detail pane
      viewPlayerDetails: this.props.lineup.roster[0]
    }
  },


  openPlayerDetail(playerId) {
    log.debug('openPlayerDetail() - open', playerId)
    this.setState({viewPlayerDetails: playerId})
    this.props.whichSide === 'opponent' ? AppActions.togglePlayerPane('right') : AppActions.togglePlayerPane('left')
  },


  closeLineup() {
    this.props.updatePath(vsprintf('/live/lineups/%d/contests/%d/', [this.props.mode.myLineupId, this.props.mode.contestId]))

    const newMode = Object.assign({}, this.props.mode, {
      opponentLineupId: undefined
    })

    this.props.updateLiveMode(newMode)
  },


  render() {
    const self = this
    const draftGroup = self.props.lineup.draftGroup
    const currentPlayers = self.props.lineup.roster.map(function(playerId) {
      const player = self.props.lineup.rosterDetails[playerId]
      const boxScore = self.props.currentBoxScores[player.info.game_srid]

      return (
        <LiveLineupPlayer key={playerId} player={player} whichSide={self.props.whichSide} onClick={self.openPlayerDetail.bind(self, playerId)} />
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

    let closeLineup
    if (self.props.whichSide === 'opponent') {
      closeLineup = (
        <span className="live-lineup__close" onClick={ self.closeLineup }></span>
      )
    }


    const className = 'cmp-live__lineup live-lineup live-lineup--' + self.props.whichSide

    return (
      <div className={ className }>
        { closeLineup }
        <ul className="live-lineup__players">
          {currentPlayers}
        </ul>

        { playerPane }
        <div className="view-player-detail"  />
      </div>
    )
  }
})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {}
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (newMode) => dispatch(updateLiveMode(newMode)),
    updatePath: (path) => dispatch(updatePath(path))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveLineupConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveLineup)

// Render the component.
renderComponent(
  <Provider store={store}>
    <LiveLineupConnected />
  </Provider>,
  '.live-lineup'
)

export default LiveLineupConnected



module.exports = LiveLineup
