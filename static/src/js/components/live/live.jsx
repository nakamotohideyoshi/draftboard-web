import * as ReactRedux from 'react-redux'
import _ from 'lodash'
import createBrowserHistory from 'history/lib/createBrowserHistory'
import Pusher from 'pusher-js'
import React from 'react'
import renderComponent from '../../lib/render-component'
import { Router, Route } from 'react-router'
import { syncReduxAndRouter } from 'redux-simple-router'
import { updatePath } from 'redux-simple-router'

import LiveBottomNav from './live-bottom-nav'
import LiveContestsPane from './live-contests-pane'
import LiveCountdown from './live-countdown'
import LiveHeader from './live-header'
import LiveLineup from './live-lineup'
import LiveLineupSelectModal from './live-lineup-select-modal'
import LiveMoneyline from './live-moneyline'
import LiveNBACourt from './live-nba-court'
import LiveStandingsPaneConnected from './live-standings-pane'

import { navScoreboardSelector } from '../../selectors/nav-scoreboard'
import log from '../../lib/logging'
import store from '../../store'
import { liveContestsStatsSelector } from '../../selectors/live-contests'
import { currentLineupsStatsSelector } from '../../selectors/current-lineups'
import { liveSelector } from '../../selectors/live'
import { updatePlayerStats } from '../../actions/live-draft-groups'
import { updateLiveMode } from '../../actions/live'
import { updateBoxScore } from '../../actions/current-box-scores'


// Set up to make sure that push states are synced with redux substore
const history = createBrowserHistory()
syncReduxAndRouter(history, store)

/**
 * The overarching component for the live section.
 *
 * Connects with the LiveStore for data.
 * This will be where the state changes and then properties are cascaded down to the other child components.
 */
const Live = React.createClass({

  propTypes: {
    // redux selectors
    currentLineupsStats: React.PropTypes.object.isRequired,
    liveContestsStats: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    navScoreboardStats: React.PropTypes.object.isRequired,

    // react router URL params
    params: React.PropTypes.object,

    // imported functions
    fetchContestLineupsUsernamesIfNeeded: React.PropTypes.func,
    updateBoxScore: React.PropTypes.func,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },

  changePathAndMode(path, changedFields) {
    log.debug('Live.changePathAndMode()', path)

    // update the URL path
    this.props.updatePath(path)

    // update redux store mode
    this.props.updateLiveMode(changedFields)

    // if the contest has changed, then get the appropriate usernames for the standings pane
    if (changedFields.hasOwnProperty('contestId')) {
      this.props.fetchContestLineupsUsernamesIfNeeded(changedFields.contestId)
    }
  },

  getInitialState() {
    return {
      courtEvents: {},
      eventDescriptions: {},
      gameQueues: {},
      playersPlaying: [],
      relevantPlayerHistory: {}
    }
  },

  componentWillMount() {
    const urlParams = this.props.params

    if (urlParams.hasOwnProperty('myLineupId')) {
      this.props.updateLiveMode({
        myLineupId: urlParams.myLineupId,
        contestId: urlParams.contestId || undefined,
        opponentLineupId: urlParams.opponentLineupId || undefined
      })
    }

    this.listenToSockets()
  },

  listenToSockets() {
    log.debug('listenToSockets()')
    const self = this

    // NOTE: this really bogs down your console
    // Pusher.log = function(message) {
    //   if (window.console && window.console.log) {
    //     window.console.log(message);
    //   }
    // };

    const pusher = new Pusher(window.dfs.user.pusher_key, {
      encrypted: true
    })

    const channelPrefix = window.dfs.user.pusher_channel_prefix.toString()
    const nbaPBPChannel = pusher.subscribe(channelPrefix + 'nba_pbp')
    nbaPBPChannel.bind('event', (eventData) => {
      self.onPBPReceived(eventData)
    })

    const nbaStatsChannel = pusher.subscribe(channelPrefix + 'nba_stats')
    nbaStatsChannel.bind('player', (eventData) => {
      self.onStatsReceived(eventData)
    })

    const boxscoresChannel = pusher.subscribe(channelPrefix + 'boxscores')
    boxscoresChannel.bind('team', (eventData) => {
      self.onBoxscoreReceived(eventData)
    })
  },

  onStatsReceived(eventCall) {
    log.debug('onStatsReceived()')
    const self = this
    const gameId = eventCall.srid_game

    // for now, only use calls once data is loaded
    if (self.props.liveSelector.hasRelatedInfo === false) {
      return
    }

    // if relevant game, then add to game queue
    if (self.props.liveSelector.relevantGames.indexOf(gameId) === -1) {
      // copy to keep immutable
      let gameQueues = Object.assign({}, self.state.gameQueues)
      // get game queue related to event
      let gameQueue = {
        isRunning: false,
        queue: []
      }
      if (gameId in gameQueues) {
        gameQueue = gameQueues[gameId]
      }

      // add in new event to the end of the queue
      gameQueue.queue.push({
        type: 'stats',
        event: eventCall
      })
      gameQueues[gameId] = gameQueue
      self.setState({gameQueues: gameQueues})

      // if the queue isn't already running, start it up
      if (gameQueue.isRunning === false) {
        self.popOldestGameEvent(gameId)
      }

      return
    }

    // otherwise just update the player's FP
    self.props.updatePlayerStats(
      eventCall.fields.player_id,
      eventCall,
      self.props.liveSelector.lineups.mine.draftGroup.id
    )
  },

  onBoxscoreReceived(eventCall) {
    log.debug('onBoxscoreReceived()')
    const self = this

    // for now, only use calls once data is loaded
    if (self.props.liveSelector.hasRelatedInfo === false) {
      return
    }

    // check that it's a boxscore we care about
    if (eventCall.game__id in self.props.navScoreboardStats.sports.games === false || 'points' in eventCall === false) {
      log.debug('onBoxscoreReceived() - not a relevant event', eventCall)
      return false
    }

    if ('boxscore' in self.props.navScoreboardStats.sports[eventCall.game__id] === false) {
      log.debug('onBoxscoreReceived() - game not started')
      return false
    }

    // copy to keep immutable
    let gameQueues = Object.assign({}, self.state.gameQueues)
    const gameId = eventCall.game__id

    // get game queue related to event
    let gameQueue = {
      isRunning: false,
      queue: []
    }
    if (gameId in gameQueues) {
      gameQueue = gameQueues[gameId]
    }

    // add in new event to the end of the queue
    gameQueue.queue.push({
      type: 'boxscore',
      event: eventCall
    })
    gameQueues[gameId] = gameQueue
    self.setState({gameQueues: gameQueues})

    // if the queue isn't already running, start it up
    if (gameQueue.isRunning === false) {
      self.popOldestGameEvent(gameId)
    }
  },

  onPBPReceived(eventCall) {
    log.debug('onPBPReceived()')
    const self = this

    // for now, only use calls once data is loaded
    if (self.props.liveSelector.hasRelatedInfo === false) {
      return
    }

    // if this is not a statistical based call, ignore
    if ('statistics__list' in eventCall === false) {
      log.debug('onPBPReceived() - had no statistics__list', eventCall)
      return false
    }

    const events = eventCall.statistics__list
    const gameId = eventCall.game__id

    if (gameId === undefined) {
      log.warn('gameId did not exist for this PBP, yet had a relevantPlayer', eventCall)
      return false
    }

    // get game queue related to event
    let gameQueue = {
      isRunning: false,
      queue: []
    }
    if (gameId in self.state.gameQueues) {
      gameQueue = self.state.gameQueues[gameId]
    }

    // loop through players to see if they match one of the players in the lineups
    _.forEach(events, function(event) {
      if (self.props.liveSelector.relevantPlayers.indexOf(event.player) !== -1) {
        log.debug('onPBPReceived() player found', event.player)

        // copy to keep immutable
        let gameQueues = Object.assign({}, self.state.gameQueues)

        // add in new event to the end of the queue
        gameQueue.queue.push({
          type: 'pbp',
          event: eventCall
        })
        gameQueues[gameId] = gameQueue
        self.setState({gameQueues: gameQueues})

        // if the queue isn't already running, start it up
        if (gameQueue.isRunning === false) {
          self.popOldestGameEvent(gameId)
        }
      }
    })
  },

  popOldestGameEvent(gameId) {
    log.debug('popOldestGameEvent')
    const self = this

    // copy to keep immutable
    let gameQueues = Object.assign({}, self.state.gameQueues)

    let gameQueue = gameQueues[gameId]
    gameQueue.isRunning = true
    log.debug('gameQueue length', gameQueue.queue.length)

    // if there are no more events, then stop running
    if (gameQueue.queue.length === 0) {
      gameQueue.isRunning = false

      self.setState({gameQueues: gameQueues})
      return false
    }

    // pop oldest event
    const oldestEvent = gameQueue.queue.shift()
    const eventCall = oldestEvent.event

    // update state with updated queue
    self.setState({gameQueues: gameQueues})

    // depending on what type of data, either show animation on screen or update stats
    switch (oldestEvent.type) {
      // if this is a court animation, then start er up
      case 'pbp':
        self.showGameEvent(eventCall)
        log.info('showGameEvent(), queue of ', gameQueue.queue.length, eventCall)
        break

      // if boxscore, then update the boxscore data
      case 'boxscore':
        self.props.updateBoxScore(
          eventCall.game__id,
          eventCall.id,
          eventCall.points
        )

        // then move on to the next
        self.popOldestGameEvent(gameId)
        break

      case 'stats':
        const players = self.props.liveSelector.draftGroup.playersInfo

        let name = 'Unknown'
        if (eventCall.fields.player_id in players) {
          name = players[eventCall.fields.player_id].name
        }
        log.info('Live.popOldestGameEvent().updatePlayerStats()', name, eventCall)

        self.props.updatePlayerStats(
          eventCall.fields.player_id,
          eventCall,
          self.props.liveSelector.lineups.mine.draftGroup.id
        )

        // then move on to the next
        self.popOldestGameEvent(gameId)
    }
  },

  showGameEvent(eventCall) {
    log.debug('showGameEvent()', eventCall)

    const self = this
    const relevantPlayers = self.props.liveSelector.relevantPlayers

    let players = []
    let playersPlaying = self.state.playersPlaying.slice(0)

    // relevant information for court animation
    let courtInformation = {
      'id': eventCall.id,
      'location': eventCall.location__list,
      'events': {}
    }

    // for now limit to one event per statistical event
    _.forEach(eventCall.statistics__list, function(event, key) {
      // if the player applies to our lineups
      if (relevantPlayers.indexOf(event.player) !== -1) {
        players.push(event.player)
        playersPlaying.push(event.player)

        // set which side to show this event set on
        courtInformation.whichSide = 'mine'

        if (self.props.liveSelector.mode.opponentLineupId) {
          if (self.props.liveSelector.lineups.opponent.rosterBySRID.indexOf(event.player) > -1) {
            courtInformation.whichSide = 'opponent'
          }

          if (self.props.liveSelector.playersInBothLineups.indexOf(event.player) > -1) {
            courtInformation.whichSide = 'both'
          }
        }
      }

      courtInformation.events[key.slice(0, -6)] = event
    })
    log.debug('potential playersPlaying', playersPlaying)
    self.setState({playersPlaying: playersPlaying})

    log.debug('setTimeout - animate on court')

    let courtEvents = Object.assign({}, self.state.courtEvents)
    courtEvents[courtInformation.id] = courtInformation
    self.setState({courtEvents: courtEvents})

    // show the results
    setTimeout(function() {
      log.debug('setTimeout - show the results')

      // remove players from playersPlaying
      let playersPlaying = self.state.playersPlaying.slice[0]

      playersPlaying = _.remove(playersPlaying, (value) => {
        return players.indexOf(value) === -1
      })
      self.setState({playersPlaying: playersPlaying})

      // update player fp
      _.forEach(eventCall.statistics__list, function(event, key) {
        // show event description
        const eventDescription = {
          points: '?',
          info: eventCall.description,
          when: eventCall.clock
        }

        // TODO modify this once pbp has player stats built in
        let eventDescriptions = Object.assign(
          {},
          self.state.eventDescriptions,
          {
            [event.player]: eventDescription
          }
        )
        self.setState({ eventDescriptions: eventDescriptions })

        // update history to have relevant player
        let relevantPlayerHistory = Object.assign({}, self.state.relevantPlayerHistory)

        if (self.state.relevantPlayerHistory.hasOwnProperty(event.player) === false) {
          relevantPlayerHistory[event.player] = []
        }

        // add event to player's history
        relevantPlayerHistory[event.player].push(eventDescription)
        self.setState({ relevantPlayerHistory: relevantPlayerHistory })

        setTimeout(function() {
          log.debug('setTimeout - remove event description')
          let eventDescriptions = Object.assign({}, self.state.eventDescriptions)


          delete(eventDescriptions[event.player])
          self.setState({ eventDescriptions: eventDescriptions })
        }, 4000)
      })

    }.bind(this), 3000)

    // remove the player from the court
    setTimeout(function() {
      log.debug('setTimeout - remove the player from the court')
      let courtEvents = Object.assign({}, self.state.courtEvents)
      delete courtEvents[courtInformation.id]
      self.setState({courtEvents: courtEvents})
    }.bind(this) , 7000)

    // enter the next item in the queue
    setTimeout(function() {
      self.popOldestGameEvent(eventCall.game__id)
    }.bind(this), 9000)
  },

  renderLoadingScreen() {
    return (<div />)
  },

  render() {
    const liveSelector = this.props.liveSelector
    const mode = liveSelector.mode

    // defining optional component pieces
    let
      liveStandingsPane,
      moneyLine,
      opponentLineupComponent

    // wait for data to load before showing anything
    if (liveSelector.hasRelatedInfo === false) {
      return this.renderLoadingScreen()
    }

    // if a lineup has not been chosen yet
    if (mode.hasOwnProperty('myLineupId') === false) {
      return (
        <LiveLineupSelectModal
          changePathAndMode={this.changePathAndMode}
          lineups={this.props.currentLineupsStats} />
      )
    }

    // wait until the lineup data has loaded before rendering
    if (liveSelector.lineups.hasOwnProperty('mine')) {
      const myLineup = liveSelector.lineups.mine

      // show the countdown until it goes live
      if (myLineup.roster === undefined) {
        return (
          <LiveCountdown lineup={myLineup} />
        )
      }

      // if viewing a contest, then add standings pane and moneyline
      if (mode.contestId) {
        const contest = liveSelector.contest
        let opponentWinPercent

        liveStandingsPane = (
          <LiveStandingsPaneConnected
            changePathAndMode={this.changePathAndMode}
            contest={contest}
            lineups={contest.lineups}
            rankedLineups={contest.rankedLineups}
            mode={mode} />
        )

        // if viewing an opponent, add in lineup and update moneyline
        if (mode.opponentLineupId) {
          const opponentLineup = liveSelector.lineups.opponent
          opponentWinPercent = opponentLineup.opponentWinPercent

          opponentLineupComponent = (
            <LiveLineup
              changePathAndMode={this.changePathAndMode}
              eventDescriptions={this.state.eventDescriptions}
              games={this.props.navScoreboardStats.sports.games}
              lineup={opponentLineup}
              mode={mode}
              playersPlaying={this.state.playersPlaying}
              relevantPlayerHistory={this.state.relevantPlayerHistory}
              whichSide="opponent" />
          )
        }

        moneyLine = (
          <section className="live-winning-graph live-winning-graph--contest-overall">
            <LiveMoneyline
              percentageCanWin={contest.percentageCanWin}
              myWinPercent={myLineup.myWinPercent}
              opponentWinPercent={opponentWinPercent} />
          </section>
        )
      }

      return (
        <div>
          <LiveLineup
            changePathAndMode={this.changePathAndMode}
            eventDescriptions={this.state.eventDescriptions}
            games={this.props.navScoreboardStats.sports.games}
            lineup={myLineup}
            mode={mode}
            playersPlaying={this.state.playersPlaying}
            relevantPlayerHistory={this.state.relevantPlayerHistory}
            whichSide="mine" />

          {opponentLineupComponent}

          <section className="cmp-live__court-scoreboard">
            <LiveHeader
              changePathAndMode={this.changePathAndMode}
              liveSelector={liveSelector} />

            <LiveNBACourt
              liveSelector={liveSelector}
              courtEvents={this.state.courtEvents} />

            { moneyLine }

            <LiveBottomNav
              hasContest={mode.contestId !== undefined} />

          </section>

          <LiveContestsPane
            changePathAndMode={this.changePathAndMode}
            lineup={myLineup}
            mode={mode} />

          { liveStandingsPane }
        </div>
      )
    }

    // TODO Live - make a loading screen if it takes longer than a second to load
    return this.renderLoadingScreen()
  }

})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    // selectors
    currentLineupsStats: currentLineupsStatsSelector(state),
    liveContestsStats: liveContestsStatsSelector(state),
    liveSelector: liveSelector(state),
    navScoreboardStats: navScoreboardSelector(state)
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateBoxScore: (gameId, teamId, points) => dispatch(updateBoxScore(gameId, teamId, points)),
    updatePlayerStats: (eventCall, draftGroupId, playerId, fp) => dispatch(updatePlayerStats(eventCall, draftGroupId, playerId, fp)),
    updateLiveMode: (type, id) => dispatch(updateLiveMode(type, id)),
    updatePath: (path) => dispatch(updatePath(path))
  }
}

// Wrap the component to inject dispatch and selected state into it.
const LiveConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Live)

renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/live/" component={LiveConnected} />
      <Route path="/live/lineups/:myLineupId" component={LiveConnected} />
      <Route path="/live/lineups/:myLineupId/contests/:contestId/" component={LiveConnected} />
      <Route path="/live/lineups/:myLineupId/contests/:contestId/opponents/:opponentLineupId" component={LiveConnected} />
    </Router>
  </Provider>,
  '.cmp-live'
)
