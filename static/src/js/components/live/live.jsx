import * as ReactRedux from 'react-redux'
import _ from 'lodash'
import createBrowserHistory from 'history/lib/createBrowserHistory'
import Pusher from 'pusher-js'
import React from 'react'
import renderComponent from '../../lib/render-component'
import update from 'react-addons-update'
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
import log from '../../lib/logging'
import store from '../../store'
import { currentLineupsSelector } from '../../selectors/current-lineups'
import { fetchContestLineupsUsernamesIfNeeded } from '../../actions/live-contests'
import { fetchEntriesIfNeeded } from '../../actions/entries'
import { fetchSportsIfNeeded } from '../../actions/sports'
import { liveContestsSelector } from '../../selectors/live-contests'
import { liveSelector } from '../../selectors/live'
import { sportsSelector } from '../../selectors/sports'
import { updateGame } from '../../actions/sports'
import { updateLiveMode } from '../../actions/live'
import { updatePlayerStats } from '../../actions/live-draft-groups'


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  currentLineupsSelector: currentLineupsSelector(state),
  liveContestsSelector: liveContestsSelector(state),
  liveSelector: liveSelector(state),
  sportsSelector: sportsSelector(state),
})

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
const mapDispatchToProps = (dispatch) => ({
  fetchContestLineupsUsernamesIfNeeded: (contestId) => dispatch(fetchContestLineupsUsernamesIfNeeded(contestId)),
  fetchEntriesIfNeeded: (id) => dispatch(fetchEntriesIfNeeded(id)),
  fetchSportsIfNeeded: () => dispatch(fetchSportsIfNeeded()),
  updateGame: (gameId, teamId, points) => dispatch(updateGame(gameId, teamId, points)),
  updatePlayerStats: (eventCall, draftGroupId, playerId, fp) => dispatch(
    updatePlayerStats(eventCall, draftGroupId, playerId, fp)
  ),
  updateLiveMode: (type, id) => dispatch(updateLiveMode(type, id)),
  updatePath: (path) => dispatch(updatePath(path)),
})

/*
 * The overarching component for the live section.
 */
const Live = React.createClass({

  propTypes: {
    currentLineupsSelector: React.PropTypes.object.isRequired,
    fetchEntriesIfNeeded: React.PropTypes.func,
    fetchContestLineupsUsernamesIfNeeded: React.PropTypes.func,
    fetchSportsIfNeeded: React.PropTypes.func,
    liveContestsSelector: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    params: React.PropTypes.object,
    sportsSelector: React.PropTypes.object.isRequired,
    updateGame: React.PropTypes.func,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func,
    updatePlayerStats: React.PropTypes.func,
  },

  getInitialState() {
    return {
      courtEvents: {},
      eventDescriptions: {},
      playersPlaying: [],
      relevantPlayerHistory: {},
    };
  },

  componentWillMount() {
    const urlParams = this.props.params

    if (urlParams.hasOwnProperty('myLineupId')) {
      this.props.updateLiveMode({
        myLineupId: urlParams.myLineupId,
        contestId: urlParams.contestId || undefined,
        opponentLineupId: urlParams.opponentLineupId || undefined,
      })
    }

    this.listenToSockets()
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to our games, and if so send to the appropriate queue
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onBoxscoreReceived(eventCall) {
    log.debug('Live.onBoxscoreReceived()')
    const gameId = eventCall.game__id

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return
    }

    // if the event didn't involve points, then don't bother bc that's all we deal with
    if (eventCall.hasOwnProperty('points') === false) {
      log.debug('Live.onBoxscoreReceived() - call had no points', eventCall)
      return
    }

    this.addEventAndStartQueue(eventCall.game__id, eventCall, 'boxscore')
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to one the relevant players
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onPBPReceived(eventCall) {
    log.debug('Live.onPBPReceived()')
    const gameId = eventCall.game__id

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return
    }

    // if this is not a statistical based call, ignore
    if ('statistics__list' in eventCall === false) {
      log.debug('Live.onPBPReceived() - had no statistics__list', eventCall)
      return
    }

    const relevantPlayers = this.props.liveSelector.relevantPlayers
    const eventPlayers = _.map(eventCall.statistics__list, event => event.player)

    // only add to the queue if we care about the player(s)
    if (_.intersection(relevantPlayers, eventPlayers).length > 0) {
      this.addEventAndStartQueue(gameId, eventCall, 'pbp')
    }
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to our games/players, and if so send to the appropriate
   * method to be parsed
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onStatsReceived(eventCall) {
    log.debug('Live.onStatsReceived()')
    const gameId = eventCall.srid_game

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return
    }

    // if it's not a relevant game to the live section, then just update the player's FP to update the NavScoreboard
    if (this.props.liveSelector.relevantGames.indexOf(gameId) !== -1) {
      // otherwise just update the player's FP
      this.props.updatePlayerStats(
        eventCall.fields.player_id,
        eventCall,
        this.props.liveSelector.lineups.mine.draftGroup.id
      )
      return
    }

    this.addEventAndStartQueue(gameId, eventCall, 'stats')
  },

  /*
   * Helper method to add a new Pusher event to the appropriate state.[gameId] queue and then start the queue up
   *
   * @param {integer} gameId Game SRID to determine game queue
   * @param {object} event The json object received from Pusher
   * @param {string} type The type of call, options are 'stats', 'php', 'boxscore'
   */
  addEventAndStartQueue(gameId, event, type) {
    log.debug('Live.addEventAndStartQueue', gameId, event, type)

    // set up game queue event
    const gameQueueEvent = {
      type,
      event,
    }

    // get game queue related to event, otherwise make a new one
    // then start up queue if it isn't running
    if (this.state.hasOwnProperty(gameId)) {
      this.setState({
        [gameId]: update(this.state[gameId], {
          queue: {
            $push: [gameQueueEvent],
          },
        }),
      })

      if (this.state[gameId].isRunning === false) this.shiftOldestGameEvent(gameId)
    } else {
      this.setState({
        [gameId]: {
          isRunning: false,
          queue: [gameQueueEvent],
        },
      })

      this.shiftOldestGameEvent(gameId)
    }
  },

  /*
   * Since we base the live section on the redux store.live substore, we have to have this method to update both the
   * redux substore AND the url push state, so a user can go "back"
   * @param  {string} path The URL path to push
   * @param  {object} changedFields The changed fields in store.live substore
   */
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

  /**
   * Force a refresh fo draft groups. Called by the countdown when time is up
   */
  forceDraftGroupRefresh() {
    log.info('Live.forceDraftGroupRefresh()')
    this.props.fetchEntriesIfNeeded(true)
  },

  /*
   * Start up Pusher listeners to the necessary channels and events
   */
  listenToSockets() {
    log.info('Live.listenToSockets()')

    // NOTE: this really bogs down your console, only use locally when needed
    // uncomment this ONLY if you need to debug why Pusher isn't connecting
    // Pusher.log = function(message) {
    //   if (window.console && window.console.log) {
    //     window.console.log(message);
    //   }
    // };

    const pusher = new Pusher(window.dfs.user.pusher_key, {
      encrypted: true,
    })

    // used to separate developers into different channels, based on their django settings filename
    const channelPrefix = window.dfs.user.pusher_channel_prefix.toString()

    const nbaPBPChannel = pusher.subscribe(`${channelPrefix}nba_pbp`)
    nbaPBPChannel.bind('event', this.onPBPReceived)

    const nbaStatsChannel = pusher.subscribe(`${channelPrefix}nba_stats`)
    nbaStatsChannel.bind('player', this.onStatsReceived)

    const boxscoresChannel = pusher.subscribe(`${channelPrefix}boxscores`)
    boxscoresChannel.bind('team', this.onBoxscoreReceived)
  },

  /*
   * Check whether the Pusher call has the right information we need
   *
   * @return {Boolean} Whether the event is relevant to the live/nav sections
   */
  isPusherEventRelevant(eventCall, gameId) {
    // for now, only use calls once data is loaded
    if (this.props.liveSelector.hasRelatedInfo === false) {
      log.trace('Live.isPusherEventRelevant() - hasRelatedInfo === false', eventCall)
      return false
    }

    const games = this.props.sportsSelector.games

    // check that the game is relevant
    if (games.hasOwnProperty(gameId) === false) {
      log.trace('eventCall had irrelevant game', eventCall)
      return false
    }

    // if we haven't received from the server that the game has started, then ask the server for an update!
    if (games[gameId].hasOwnProperty('boxscore') === false) {
      log.trace('Live.onBoxscoreReceived() - related game had no boxscore from server', eventCall)
      this.props.fetchSportsIfNeeded()
      return false
    }

    return true
  },

  /*
   * This takes the oldest event in a given game queue, from state.gameQueues, and then uses the data, whether it is to
   * animate if a pbp, or update redux stats.
   *
   * @param  {string} gameId The game queue SRID to pop the oldest event
   */
  shiftOldestGameEvent(gameId) {
    const gameQueue = Object.assign({}, this.state[gameId])

    // if there are no more events, then stop running
    if (gameQueue.queue.length === 0) {
      gameQueue.isRunning = false

      this.setState({ [gameId]: gameQueue })
      return
    }

    // pop oldest event
    const oldestEvent = gameQueue.queue.shift()
    const eventCall = oldestEvent.event

    log.info(`Live.shiftOldestGameEvent(), game ${gameId}, queue of ${gameQueue.queue.length}`, eventCall)

    // update state with updated queue
    gameQueue.isRunning = true
    this.setState({ [gameId]: gameQueue })

    // depending on what type of data, either show animation on screen or update stats
    switch (oldestEvent.type) {

      // if this is a court animation, then start er up
      case 'pbp':
        this.showGameEvent(eventCall)
        break

      // if boxscore, then update the boxscore data
      case 'boxscore':
        this.props.updateGame(
          eventCall.game__id,
          eventCall.id,
          eventCall.points
        )

        // then move on to the next
        this.shiftOldestGameEvent(gameId)
        break

      // if stats, then update the player stats
      case 'stats':
        const players = this.props.liveSelector.draftGroup.playersInfo
        const player = players[eventCall.fields.playerId] || {}

        log.info('Live.shiftOldestGameEvent().updatePlayerStats()', player.name || 'Unknown', eventCall)

        this.props.updatePlayerStats(
          eventCall.fields.player_id,
          eventCall,
          this.props.liveSelector.lineups.mine.draftGroup.id
        )

        // then move on to the next
        this.shiftOldestGameEvent(gameId)
        break

      // no default
      default:
        return
    }
  },

  /*
   * Show a game event from a Pusher pbp call in the court and in the player information
   * @param  {object} eventCall The event call to parse for information
   */
  showGameEvent(eventCall) {
    // relevant information for court animation
    const courtEvent = {
      location: eventCall.location__list,
      id: eventCall.id,
      whichSide: 'mine',
    }

    const relevantPlayers = this.props.liveSelector.relevantPlayers
    const eventPlayers = _.map(eventCall.statistics__list, event => event.player)
    const relevantPlayersInEvent = _.intersection(relevantPlayers, eventPlayers)

    // determine what color the animation should be, based on which lineup(s) the player(s) are in
    if (this.props.liveSelector.mode.opponentLineupId) {
      const rosterBySRID = this.props.liveSelector.lineups.opponent.rosterBySRID
      const playersInBothLineups = this.props.liveSelector.playersInBothLineups

      if (_.intersection(rosterBySRID, relevantPlayersInEvent).length > 0) {
        courtEvent.whichSide = 'opponent'
      }
      if (_.intersection(playersInBothLineups, relevantPlayersInEvent).length > 0) {
        courtEvent.whichSide = 'both'
      }
    }

    // update state to reflect players playing and court events
    this.setState({
      courtEvents: update(this.state.courtEvents, {
        $merge: {
          [courtEvent.id]: courtEvent,
        },
      }),
      playersPlaying: _.union(this.state.playersPlaying, relevantPlayersInEvent),
    })

    // show the results
    setTimeout(() => {
      log.debug('setTimeout - show the results')

      // remove relevant event players from players playing
      this.setState({ playersPlaying: _.difference(this.state.playersPlaying, relevantPlayersInEvent) })

      // show event beside player and in their history
      _.forEach(relevantPlayersInEvent, (playerId) => {
        // update history to have relevant player
        const relevantPlayerHistory = Object.assign({}, this.state.relevantPlayerHistory)
        const playerHistory = relevantPlayerHistory[playerId] || []

        // set up event description
        const eventDescription = {
          points: '?',
          info: eventCall.description,
          when: eventCall.clock,
        }

        // show event beside player
        this.setState({
          eventDescriptions: update(this.state.eventDescriptions, {
            $set: {
              [playerId]: eventDescription,
            },
          }),
        })

        // add event to player history
        playerHistory.push(eventDescription)
        this.setState({
          relevantPlayerHistory: update(relevantPlayerHistory, {
            $set: {
              [playerId]: playerHistory,
            },
          }),
        })

        // remove the event beside the player when done
        setTimeout(() => {
          log.debug('setTimeout - remove event description')
          const eventDescriptions = Object.assign({}, this.state.eventDescriptions)
          delete(eventDescriptions[playerId])
          this.setState({ eventDescriptions })
        }, 4000)
      })
    }, 3000)

    // remove the animation
    setTimeout(() => {
      log.debug('setTimeout - remove the player from the court')
      const courtEvents = Object.assign({}, this.state.courtEvents)
      delete courtEvents[courtEvent.id]
      this.setState({ courtEvents })
    }, 7000)

    // enter the next item in the queue once everything is done
    setTimeout(() => {
      this.shiftOldestGameEvent(eventCall.game__id)
    }, 9000)
  },

  /*
   * This loading screen shows in lieu of the live section when it takes longer than a second to do an initial load
   * TODO Live - get built out
   *
   * @return {JSXElement}
   */
  renderLoadingScreen() {
    return (<div />)
  },

  render() {
    const liveData = this.props.liveSelector
    const mode = liveData.mode

    // defining optional component pieces
    let liveStandingsPane
    let moneyLine
    let opponentLineupComponent

    // wait for data to load before showing anything
    if (liveData.hasRelatedInfo === false) {
      return this.renderLoadingScreen()
    }

    // if a lineup has not been chosen yet
    if (mode.hasOwnProperty('myLineupId') === false) {
      return (
        <LiveLineupSelectModal
          changePathAndMode={this.changePathAndMode}
          lineups={this.props.currentLineupsSelector}
        />
      )
    }

    // wait until the lineup data has loaded before rendering
    if (liveData.lineups.hasOwnProperty('mine')) {
      const myLineup = liveData.lineups.mine

      // show the countdown until it goes live
      if (myLineup.roster === undefined) {
        return (
          <LiveCountdown
            onCountdownComplete={this.forceDraftGroupRefresh}
            lineup={myLineup}
          />
        )
      }

      // if viewing a contest, then add standings pane and moneyline
      if (mode.contestId) {
        const contest = liveData.contest
        let opponentWinPercent

        liveStandingsPane = (
          <LiveStandingsPaneConnected
            changePathAndMode={this.changePathAndMode}
            contest={contest}
            lineups={contest.lineups}
            rankedLineups={contest.rankedLineups}
            mode={mode}
          />
        )

        // if viewing an opponent, add in lineup and update moneyline
        if (mode.opponentLineupId) {
          const opponentLineup = liveData.lineups.opponent
          opponentWinPercent = opponentLineup.opponentWinPercent

          opponentLineupComponent = (
            <LiveLineup
              changePathAndMode={this.changePathAndMode}
              eventDescriptions={this.state.eventDescriptions}
              games={this.props.sportsSelector.games}
              lineup={opponentLineup}
              mode={mode}
              playersPlaying={this.state.playersPlaying}
              relevantPlayerHistory={this.state.relevantPlayerHistory}
              whichSide="opponent"
            />
          )
        }

        moneyLine = (
          <section className="live-moneyline live-moneyline--contest-overall">
            <LiveMoneyline
              percentageCanWin={contest.percentageCanWin}
              myWinPercent={myLineup.myWinPercent}
              opponentWinPercent={opponentWinPercent}
            />
          </section>
        )
      }

      return (
        <div>
          <LiveLineup
            changePathAndMode={this.changePathAndMode}
            eventDescriptions={this.state.eventDescriptions}
            games={this.props.sportsSelector.games}
            lineup={myLineup}
            mode={mode}
            playersPlaying={this.state.playersPlaying}
            relevantPlayerHistory={this.state.relevantPlayerHistory}
            whichSide="mine"
          />

          {opponentLineupComponent}

          <section className="cmp-live__court-scoreboard">
            <LiveHeader
              changePathAndMode={this.changePathAndMode}
              liveSelector={liveData}
            />

            <LiveNBACourt
              liveSelector={liveData}
              courtEvents={this.state.courtEvents}
            />

            {moneyLine }

            <LiveBottomNav
              hasContest={mode.contestId !== undefined}
            />

          </section>

          <LiveContestsPane
            changePathAndMode={this.changePathAndMode}
            lineup={myLineup}
            mode={mode}
          />

          {liveStandingsPane }
        </div>
      )
    }

    // TODO Live - make a loading screen if it takes longer than a second to load
    return this.renderLoadingScreen()
  },
})

// Set up Redux connections to React
const { Provider, connect } = ReactRedux

// Wrap the component to inject dispatch and selected state into it.
const LiveConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Live)

// Set up to make sure that push states are synced with redux substore
const history = createBrowserHistory()
syncReduxAndRouter(history, store)

// Uses the Provider and Routes in order to have URL routing via redux-simple-router and redux state
renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/live/" component={LiveConnected} />
      <Route path="/live/lineups/:myLineupId" component={LiveConnected} />
      <Route path="/live/lineups/:myLineupId/contests/:contestId/" component={LiveConnected} />
      <Route
        path="/live/lineups/:myLineupId/contests/:contestId/opponents/:opponentLineupId"
        component={LiveConnected}
      />
    </Router>
  </Provider>,
  '.cmp-live'
)
