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
    games: React.PropTypes.object.isRequired,
    eventDescriptions: React.PropTypes.object.isRequired,
    relevantPlayerHistory: React.PropTypes.object.isRequired,
    playersPlaying: React.PropTypes.array.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },

  getInitialState() {
    const viewPlayerDetails = this.props.lineup.length > 0 ? this.props.lineup.roster[0] : undefined
    return {
      // When true, render and show the detail pane
      viewPlayerDetails: viewPlayerDetails
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

    let currentPlayers,
        playerPane,
        closeLineup

    if (this.props.lineup.roster.length > 0) {

      currentPlayers = self.props.lineup.roster.map(function(playerId) {
        const player = self.props.lineup.rosterDetails[playerId]
        const boxScore = self.props.games[player.info.game_srid]

        return (
          <LiveLineupPlayer
            key={playerId}
            player={player}
            playersPlaying={ self.props.playersPlaying }
            eventDescriptions={ self.props.eventDescriptions }
            whichSide={self.props.whichSide}
            onClick={self.openPlayerDetail.bind(self, playerId)} />
        )
      })

      if (self.state.viewPlayerDetails) {
        let playerId = self.state.viewPlayerDetails

        // if the lineup changed, update the default player details pane
        if (self.props.lineup.roster.indexOf(self.state.viewPlayerDetails) === -1) {
          playerId = self.props.lineup.roster[0]
          self.setState({viewPlayerDetails: self.props.lineup.roster[0] })
        }

        const player = self.props.lineup.rosterDetails[playerId]
        const game = self.props.games[player.info.game_srid] || {}
        const history = self.props.relevantPlayerHistory[player.info.player_srid] || []

        playerPane = (
          <LivePlayerPane
            whichSide={self.props.whichSide}
            player={player}
            eventHistory={ history }
            game={game} />
        )
      }

      if (self.props.whichSide === 'opponent') {
        closeLineup = (
          <span className="live-lineup__close" onClick={ self.closeLineup }></span>
        )
      }
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
