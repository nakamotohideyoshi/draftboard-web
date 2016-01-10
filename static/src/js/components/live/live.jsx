import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import { Router, Route } from 'react-router'
import createBrowserHistory from 'history/lib/createBrowserHistory'
import { syncReduxAndRouter } from 'redux-simple-router'
import { updatePath } from 'redux-simple-router'
import { vsprintf } from 'sprintf-js'
import Pusher from 'pusher-js'
import _ from 'lodash'

import * as AppActions from '../../stores/app-state-store'
import errorHandler from '../../actions/live-error-handler'
import LiveContestsPaneConnected from '../live/live-contests-pane'
import LiveLineup from './live-lineup'
import LiveLineupSelectModal from './live-lineup-select-modal'
import LiveNBACourt from './live-nba-court'
import LiveOverallStats from './live-overall-stats'
import LiveStandingsPaneConnected from '../live/live-standings-pane'
import log from '../../lib/logging'
import store from '../../store'
import { fetchContestLineupsUsernamesIfNeeded } from '../../actions/live-contests'
import { liveContestsStatsSelector } from '../../selectors/live-contests'
import { currentLineupsStatsSelector } from '../../selectors/current-lineups'
import { liveSelector } from '../../selectors/live'
import { updatePlayerFP } from '../../actions/live-draft-groups'
import { updateLiveMode } from '../../actions/live'
import { updateBoxScore } from '../../actions/current-box-scores'


const history = createBrowserHistory()
syncReduxAndRouter(history, store)


/**
 * The overarching component for the live  section.
 *
 * Connects with the LiveStore for data.
 * This will be where the state changes and then properties are cascaded down to the other child components.
 */
var Live = React.createClass({

  propTypes: {
    currentBoxScores: React.PropTypes.object.isRequired,
    liveContests: React.PropTypes.object.isRequired,
    liveContestsStats: React.PropTypes.object.isRequired,
    currentLineups: React.PropTypes.object.isRequired,
    currentLineupsStats: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    liveDraftGroups: React.PropTypes.object.isRequired,
    mode: React.PropTypes.object,
    params: React.PropTypes.object,
    prizes: React.PropTypes.object,
    entries: React.PropTypes.object,
    fetchContestLineupsUsernamesIfNeeded: React.PropTypes.func,
    updateBoxScore: React.PropTypes.func,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },


  getInitialState() {
    return {
      // Selected option string. SEE: `getSelectOptions`
      playersPlaying: [],
      gameQueues: {},
      courtEvents: {}
    }
  },


  componentWillMount: function() {
    const self = this
    const urlParams = self.props.params

    if ('myLineupId' in urlParams) {
      let newMode = {
        type: 'lineup',
        myLineupId: parseInt(urlParams.myLineupId)
      }

      if ('contestId' in urlParams) {
        newMode.type = 'contest'
        newMode.contestId = parseInt(urlParams.contestId)

        // make sure to get the usernames as well
        this.props.fetchContestLineupsUsernamesIfNeeded(newMode.contestId)

        if ('opponentLineupId' in urlParams) {
          newMode.opponentLineupId = parseInt(urlParams.opponentLineupId)
        }
      }

      self.props.updateLiveMode(newMode)
    }

    self.listenToSockets()
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
    log.debug('onBoxscoreReceived()')
    const self = this
    const gameId = eventCall.srid_game

    // for now, only use calls once data is loaded
    if (self.props.entries.hasRelatedInfo === false) {
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
    self.props.updatePlayerFP(
      self.props.liveSelector.lineups.mine.draftGroup.id,
      eventCall.fields.player_id,
      eventCall.fields.fantasy_points
    )
  },


  onBoxscoreReceived(eventCall) {
    log.debug('onBoxscoreReceived()')
    const self = this

    // for now, only use calls once data is loaded
    if (self.props.entries.hasRelatedInfo === false) {
      return
    }

    // check that it's a boxscore we care about
    if (eventCall.game__id in self.props.currentBoxScores === false || 'points' in eventCall === false) {
      log.debug('onBoxscoreReceived() - not a relevant event', eventCall)
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
    if (self.props.entries.hasRelatedInfo === false) {
      return
    }

    // if this is not a statistical based call, ignore
    if ('statistics__list' in eventCall === false) {
      log.debug('onPBPReceived() - had no statistics__list')
      return false
    }

    const events = eventCall.statistics__list
    const gameId = eventCall.game__id

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
    log.debug('oldestEvent', oldestEvent)

    // depending on what type of data, either show animation on screen or update stats
    switch (oldestEvent.type) {
      // if this is a court animation, then start er up
      case 'pbp':
        self.showGameEvent(eventCall)
        break

      // if boxscore, then update the boxscore data
      case 'boxscore':
        self.props.updateBoxScore(
          eventCall.game__id,
          eventCall.id,
          eventCall.points
        )
        break

      case 'stats':
        self.props.updatePlayerFP(
          self.props.liveSelector.lineups.mine.draftGroup.id,
          eventCall.fields.player_id,
          eventCall.fields.fantasy_points
        )
    }

    // update state with updated queue
    self.setState({gameQueues: gameQueues})
  },


  showGameEvent(eventCall) {
    log.debug('showGameEvent()')

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
      event.whichSide = null

      // if the player applies to our lineups
      if (relevantPlayers.indexOf(event.player) === -1) {
        players.push(event.player)
        playersPlaying.push(event.player)
        self.setState({playersPlaying: playersPlaying})

        // TODO figure out how to find out whichSide
        event.whichSide = 'mine'
      }

      courtInformation.events[key.slice(0, -6)] = event
    })

    // trigger the animation on the court first
    setTimeout(function() {
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
          if ('points' in event && 'made' in event && event.made === 'true') {
            const draftGroupId = self.props.liveSelector.lineups.mine.draftGroup.id
            const draftGroup = self.props.liveDraftGroups[draftGroupId]
            const playerId = draftGroup.playersBySRID[event.player]
            const playerStats = draftGroup.playersStats[playerId]

            self.props.updatePlayerFP(
              draftGroupId,
              playerId,
              playerStats.fp + event.points
            )
          }
        })

      }.bind(this), 2000)

      // remove the player from the court
      setTimeout(function() {
        log.debug('setTimeout - remove the player from the court')

        self.popOldestGameEvent(eventCall.game__id)

        delete courtEvents[courtInformation.id]
        self.setState({courtEvents: courtEvents})
      }.bind(this), 4000)

    }.bind(this), 1000)
  },


  toggleStandings: function() {
    AppActions.toggleLiveRightPane('appstate--live-standings-pane--open')
  },


  toggleContests: function() {
    AppActions.toggleLiveRightPane('appstate--live-contests-pane--open')
  },


  getLiveClassNames: function() {
    return this.state.classNames.reduce(function(prev, curr, i, className) {
      return prev + ' ' + className
    }, 0)
  },


  returnToLineup: function() {
    this.props.updatePath(vsprintf('/live/lineups/%d/', [this.props.mode.myLineupId]))

    const newMode = Object.assign({}, this.props.mode, {
      type: 'lineup',
      opponentLineupId: undefined,
      contestId: undefined
    })

    this.props.updateLiveMode(newMode)
  },


  render: function() {
    const self = this

    // component pieces
    let
      lineups,
      liveTitle,
      liveStandingsPane,
      moneyLine,
      bottomNavForRightPanes,
      overallStats

    const lineupNonexistant = 'myLineupId' in self.props.mode === false
    const noRelatedInfo = self.props.entries.hasRelatedInfo === false

    // if data has not loaded yet
    if (lineupNonexistant || noRelatedInfo) {
      let chooseLineup

      if (lineupNonexistant && self.props.entries.hasRelatedInfo === true) {
        chooseLineup = (
          <LiveLineupSelectModal lineups={self.props.currentLineupsStats} />
        )
      }

      return (
        <section className="cmp-live__court-scoreboard">
          <header className="cmp-live__scoreboard live-scoreboard">
            <h1 className="live-scoreboard__contest-name" />
            <div className="live-overall-stats live-overall-stats--me" />
          </header>

          <LiveNBACourt courtEvents={self.state.courtEvents} />

          { chooseLineup }
        </section>
      )
    }

    log.debug('Live component render() props', this.props)

    if ('mine' in self.props.liveSelector.lineups) {
      var myLineup = self.props.liveSelector.lineups.mine

      bottomNavForRightPanes = (
        <div className="live-right-pane-nav live-right-pane-nav--lineup">
          <div className="live-right-pane-nav__view-contests" onClick={self.toggleContests}><span>View Contests</span></div>
        </div>
      )

      liveTitle = (
        <div>
          <h2 className="live-scoreboard__lineup-name">
            &nbsp;
          </h2>
          <h1 className="live-scoreboard__contest-name">
            { myLineup.name }
          </h1>
        </div>
      )

      overallStats = (
        <LiveOverallStats
          lineup={ myLineup }
          whichSide="mine" />
      )

      lineups = (
        <LiveLineup
          whichSide="mine"
          mode={ self.props.mode }
          currentBoxScores={ self.props.currentBoxScores }
          lineup={ myLineup } />
      )
    }

    if (self.props.mode.contestId) {
      const myContest = self.props.liveSelector.contest

      bottomNavForRightPanes = (
        <div className="live-right-pane-nav live-right-pane-nav--contest">
          <div className="live-right-pane-nav__view-contests" onClick={self.toggleContests}><span>View Contests</span></div>
          <div className="live-right-pane-nav__view-standings" onClick={self.toggleStandings}><span>View Standings &amp; Ownership</span></div>
        </div>
      )

      liveTitle = (
        <div>
          <h2 className="live-scoreboard__lineup-name">
            { myLineup.name }
          </h2>
          <h1 className="live-scoreboard__contest-name">
            { myContest.name }
            <span className="live-scoreboard__close" onClick={ self.returnToLineup }></span>
          </h1>
        </div>
      )

      overallStats = (
        <LiveOverallStats
          lineup={ myLineup }
          whichSide="mine" />
      )

      const myWinPercent = myLineup.rank / myContest.entriesCount * 100

      moneyLine = (
        <section className="live-winning-graph live-winning-graph--contest-overall">
          <div className="live-winning-graph__pmr-line">
            <div className="live-winning-graph__winners" style={{ width: myContest.percentageCanWin + '%' }}></div>
            <div className="live-winning-graph__current-position" style={{ left: myWinPercent + '%' }}></div>
          </div>
        </section>
      )

      liveStandingsPane = (
        <LiveStandingsPaneConnected
          myContest={ myContest }
          lineups={ myContest.lineups }
          rankedLineups={ myContest.rankedLineups }
          mode={ self.props.mode } />
      )

      if (self.props.mode.opponentLineupId) {
        const opponentLineup = self.props.liveSelector.lineups.opponent

        lineups = (
          <div>
            { lineups }
            <LiveLineup
              whichSide="opponent"
              mode={ self.props.mode }
              currentBoxScores={ self.props.currentBoxScores }
              lineup={ opponentLineup } />
          </div>
        )

        liveTitle = (
          <div>
            <h2 className="live-scoreboard__lineup-name">
              { myLineup.name } <span className="vs">vs</span> { opponentLineup.user.username }
            </h2>
            <h1 className="live-scoreboard__contest-name">
              { myContest.name }
              <span className="live-scoreboard__close" onClick={ self.returnToLineup }></span>
            </h1>
          </div>
        )

        overallStats = (
          <div>
            { overallStats }

            <div className="live-overall-stats__vs">vs</div>

            <LiveOverallStats
              lineup={ opponentLineup }
              whichSide="opponent" />
          </div>
        )

        const opponentWinPercent = opponentLineup.rank / myContest.entriesCount * 100

        moneyLine = (
          <section className="live-winning-graph live-winning-graph--contest-overall">
            <div className="live-winning-graph__pmr-line">
              <div className="live-winning-graph__winners" style={{ width: myContest.percentageCanWin + '%' }}></div>
              <div className="live-winning-graph__current-position" style={{ left: myWinPercent + '%' }}></div>
              <div className="live-winning-graph__current-position live-winning-graph__opponent" style={{ left: opponentWinPercent + '%' }}></div>
            </div>
          </section>
        )
      }
    }

    return (
      <div>

        { lineups }

        <section className="cmp-live__court-scoreboard">
          <header className="cmp-live__scoreboard live-scoreboard">
            { liveTitle }

            { overallStats }
          </header>

          <LiveNBACourt courtEvents={self.state.courtEvents} />

          { moneyLine }
          { bottomNavForRightPanes }

        </section>

        <section className="panes">
          <LiveContestsPaneConnected
            lineup={ myLineup }
            mode={ this.props.mode } />

          { liveStandingsPane }
        </section>
      </div>
    )
  }

})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    // state elements
    currentBoxScores: state.currentBoxScores,
    currentLineups: state.currentLineups,
    entries: state.entries,
    liveContests: state.liveContests,
    liveDraftGroups: state.liveDraftGroups,
    mode: state.live.mode,
    prizes: state.prizes,

    // selectors
    currentLineupsStats: currentLineupsStatsSelector(state),
    liveContestsStats: liveContestsStatsSelector(state),
    liveSelector: liveSelector(state)
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchContestLineupsUsernamesIfNeeded: (contestId) => dispatch(fetchContestLineupsUsernamesIfNeeded(contestId)),
    updateBoxScore: (gameId, teamId, points) => dispatch(updateBoxScore(gameId, teamId, points)),
    updatePlayerFP: (draftGroupId, playerId, fp) => dispatch(updatePlayerFP(draftGroupId, playerId, fp)),
    updateLiveMode: (type, id) => dispatch(updateLiveMode(type, id)),
    updatePath: (path) => dispatch(updatePath(path))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveConnected = connect(
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

module.exports = Live
