import _ from 'lodash'
import Pusher from 'pusher-js'
import React from 'react'
import { Provider, connect } from 'react-redux'

import errorHandler from '../../actions/live-error-handler'
import log from '../../lib/logging'
import renderComponent from '../../lib/render-component'
import store from '../../store'

import { fetchCurrentDraftGroupsIfNeeded } from '../../actions/current-draft-groups'
import { fetchEntriesIfNeeded } from '../../actions/entries'
import { fetchSportsIfNeeded } from '../../actions/sports'
import { navScoreboardSelector } from '../../selectors/nav-scoreboard'
import { updateGame } from '../../actions/sports'

import NavScoreboardFilters from './nav-scoreboard-filters'
import NavScoreboardGamesList from './nav-scoreboard-games-list'
import NavScoreboardLineupsList from './nav-scoreboard-lineups-list'
import NavScoreboardLoggedOutInfo from './nav-scoreboard-logged-out-info'
import NavScoreboardLogo from './nav-scoreboard-logo'
import NavScoreboardMenu from './nav-scoreboard-menu'
import NavScoreboardSeparator from './nav-scoreboard-separator'
import NavScoreboardSlider from './nav-scoreboard-slider'
import NavScoreboardUserInfo from './nav-scoreboard-user-info'

import { TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS } from './nav-scoreboard-const'


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  navScoreboardStats: navScoreboardSelector(state),
})

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
const mapDispatchToProps = (dispatch) => ({
  errorHandler: (exception) => dispatch(errorHandler(exception)),
  fetchCurrentDraftGroupsIfNeeded: () => dispatch(fetchCurrentDraftGroupsIfNeeded()),
  fetchEntriesIfNeeded: () => dispatch(fetchEntriesIfNeeded()),
  fetchSportsIfNeeded: () => dispatch(fetchSportsIfNeeded()),
  updateGame: (gameId, teamId, points) => dispatch(updateGame(gameId, teamId, points)),
})

/*
 * The overarching component for the scoreboard spanning the top of the site.
 *
 * Most important thing to glean from this comment is that this component is the one that loads all data for the live
 * and scoreboard redux substores!
 */
const NavScoreboard = React.createClass({

  propTypes: {
    errorHandler: React.PropTypes.func.isRequired,
    fetchCurrentDraftGroupsIfNeeded: React.PropTypes.func,
    fetchEntriesIfNeeded: React.PropTypes.func,
    fetchSportsIfNeeded: React.PropTypes.func,
    navScoreboardStats: React.PropTypes.object.isRequired,
    updateGame: React.PropTypes.func,
  },

  getInitialState() {
    return {
      // Selected option string. SEE: `getSelectOptions`
      selectedOption: null,

      // Selected option type. See type constants above.
      selectedType: null,

      // Selected option key. Subtype from the main type.
      // Competition from games and null for lineups.
      selectedKey: null,

      // whether the user is logged in or not, useful for parity checks
      user: window.dfs.user,

      // boolean to make it easy to know when to show the scoreboard
      isLoaded: false,

      // whether or not we are on the live page (determines what data to load)
      isLivePage: window.location.pathname.substring(0, 6) === '/live/',
    }
  },

  /**
   * Uses promises in order to pull in all relevant data into redux, and then starts to listen for Pusher calls
   * Here's the documentation on the order in which all the data comes in https://goo.gl/uSCH0K
   */
  componentWillMount() {
    const defaultMessage = 'Our support team has been alerted of this error and will fix immediately.'

    store.dispatch(
      fetchCurrentDraftGroupsIfNeeded()
    ).catch(
      e => errorHandler(e, `#AJSDFJWI ${defaultMessage}`)
    ).then(() => {
      // if the user is logged in
      if (this.state.user.username !== '') {
        // fetch entries and all its related data
        store.dispatch(
          fetchEntriesIfNeeded()
        ).catch(
          e => errorHandler(e, `#CAISJFIE ${defaultMessage}`)
        ).then(
          this.startListening()
        )

      // otherwise just start listening
      } else {
        this.startListening()
      }
    })
  },

  /**
   * Get the options for `NavScoreboardFilters` select menu.
   * @return {Array} options key-value pairs
   */
  getSelectOptions() {
    const options = []

    _.forEach(this.props.navScoreboardStats.sports.types, (sport) => {
      options.push({
        option: `${sport} games`,
        type: TYPE_SELECT_GAMES,
        key: sport,
      })
    })

    // add in lineups if user is logged in
    if (this.state.user.username !== '') {
      options.push({
        option: 'MY LINEUPS',
        type: TYPE_SELECT_LINEUPS,
        key: 'LINEUPS',
        count: this.props.navScoreboardStats.lineups.length,
      })
    }

    return options
  },

  /**
   * Handle `NavScoreboardFilters` select menu change.
   * @param {String} selectedOption Name of the selected option
   * @param {String} selectedType Type of the selected item
   * @param {String} selectedKey Key of the selected item type
   * @return {Object} options key-value pairs
   */
  handleChangeSelection(selectedOption, selectedType, selectedKey) {
    log.trace('handleChangeSelection()', selectedOption, selectedType, selectedKey)

    this.setState({ selectedOption, selectedType, selectedKey })
  },

  /*
   * Start up Pusher listeners to the necessary channels and events
   */
  listenToSockets() {
    // let the live page do game score calls
    if (this.state.isLivePage === true) {
      return
    }

    log.info('NavScoreboard.listenToSockets()')

    // NOTE: this really bogs down your console
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

    const boxscoresChannel = pusher.subscribe(`${channelPrefix}boxscores`)
    boxscoresChannel.bind('team', (eventData) => {
      if (this.props.navScoreboardStats.sports.games.hasOwnProperty(eventData.game__id) &&
          eventData.hasOwnProperty('points')
      ) {
        this.props.updateGame(
          eventData.game__id,
          eventData.id,
          eventData.points
        )
      }
    })
  },

  /**
   * Internal method to start listening to pusher and poll for updates
   */
  startListening() {
    this.setState({ isLoaded: true })
    this.listenToSockets()
    this.startParityChecks()
  },

  /**
   * Periodically override the redux state with server data, to ensure that we have up to date data in case we missed
   * a Pusher call here or there. In time the intervals will increase, as we gain confidence in the system.
   */
  startParityChecks() {
    // whether we are logged in or not, we always need to update sports and draftgroups
    const parityChecks = {
      sports: window.setInterval(this.props.fetchSportsIfNeeded, 60000), // one minute
      currentDraftGroups: window.setInterval(this.props.fetchCurrentDraftGroupsIfNeeded, 600000),  // ten minutes
    }

    // by default, always check whether we need to load sports
    this.props.fetchSportsIfNeeded()

    // if logged in, look for entries
    if (window.dfs.user.username !== '') {
      parityChecks.entries = window.setInterval(this.props.fetchEntriesIfNeeded, 60000)  // one minute
      this.props.fetchEntriesIfNeeded()
    }

    // add the checsk to the state in case we need to clearInterval in the future
    this.setState({ boxScoresIntervalFunc: parityChecks })
  },

  /**
   * Render slider contents based on selected filter.
   */
  renderSliderContent() {
    if (this.state.selectedType === TYPE_SELECT_LINEUPS) {
      return <NavScoreboardLineupsList lineups={this.props.navScoreboardStats.lineups} />
    } else if (this.state.selectedType === TYPE_SELECT_GAMES) {
      const sport = this.props.navScoreboardStats.sports[this.state.selectedKey]
      const games = this.props.navScoreboardStats.sports.games

      return <NavScoreboardGamesList sport={sport} games={games} />
    }

    return null
  },

  render() {
    const { username, cashBalance } = window.dfs.user
    let userInfo
    let filters
    let slider

    if (this.state.isLoaded === true) {
      filters = (
        <NavScoreboardFilters
          selected={this.state.selectedOption}
          options={this.getSelectOptions()}
          onChangeSelection={this.handleChangeSelection}
        />
      )
      slider = (
        <NavScoreboardSlider type={this.state.selectedOption}>
          {this.renderSliderContent()}
        </NavScoreboardSlider>
      )
    }

    if (this.state.user.username !== '') {
      userInfo = (
        <NavScoreboardUserInfo name={username} balance={cashBalance.toFixed(2)} />
      )
    } else {
      userInfo = (
        <NavScoreboardLoggedOutInfo />
      )
    }

    return (
      <div className="inner">
        <NavScoreboardMenu />
        <NavScoreboardSeparator half />
        { userInfo }
        <NavScoreboardSeparator />
        { filters }
        { slider }
        <NavScoreboardLogo />
      </div>
    )
  },
})

// Wrap the component to inject dispatch and selected state into it.
const NavScoreboardConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(NavScoreboard)

// Uses the Provider to have redux state
renderComponent(
  <Provider store={store}>
    <NavScoreboardConnected />
  </Provider>,
  '.cmp-nav-scoreboard'
)
