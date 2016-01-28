import _ from 'lodash'
import Pusher from 'pusher-js'
import React from 'react'
import { Provider, connect } from 'react-redux'

import errorHandler from '../../actions/live-error-handler'
import log from '../../lib/logging'
import renderComponent from '../../lib/render-component'
import store from '../../store'

import { addEvent } from '../../actions/live-game-queues'
import { fetchCurrentDraftGroupsIfNeeded } from '../../actions/current-draft-groups'
import { fetchEntriesIfNeeded } from '../../actions/entries'
import { fetchEntries } from '../../actions/entries'
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


const NavScoreboard = React.createClass({

  propTypes: {
    navScoreboardStats: React.PropTypes.object.isRequired,

    addEvent: React.PropTypes.func,
    errorHandler: React.PropTypes.func.isRequired,
    fetchEntries: React.PropTypes.func,
    fetchEntriesIfNeeded: React.PropTypes.func,
    fetchSportsIfNeeded: React.PropTypes.func,
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

      user: window.dfs.user,

      isLoaded: false,

      isLivePage: window.location.pathname.substring(0, 6) === '/live/',
    }
  },

  componentWillMount() {
    if (this.state.user.username !== '') {
      store.dispatch(
        fetchCurrentDraftGroupsIfNeeded()
      ).catch(reason => {
        errorHandler(reason)
      }).then(() => {
        store.dispatch(
          fetchEntriesIfNeeded()
        ).then(() => {
          this.setState({ isLoaded: true })
          this.listenToSockets()
          this.startParityChecks()
        }).catch(reason => {
          errorHandler(
            reason,
            'Live data load failed. Our server team has been alerted and will be diagnosing this ASAP.'
          )
        })
      })
    } else {
      store.dispatch(
        fetchCurrentDraftGroupsIfNeeded()
      ).catch(reason => {
        errorHandler(reason)
      }).then(() => {
        this.setState({ isLoaded: true })

        this.listenToSockets()
        this.startParityChecks()
      })
    }
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

  listenToSockets() {
    log.debug('listenToSockets()')

    // let the live page do game score calls
    if (this.state.isLivePage === true) {
      return
    }

    // NOTE: this really bogs down your console
    // Pusher.log = function(message) {
    //   if (window.console && window.console.log) {
    //     window.console.log(message);
    //   }
    // };

    const pusher = new Pusher(window.dfs.user.pusher_key, {
      encrypted: true,
    })

    const channelPrefix = window.dfs.user.pusher_channel_prefix.toString()
    const boxscoresChannel = pusher.subscribe(`${channelPrefix}boxscores`)
    boxscoresChannel.bind('team', (eventData) => {
      if (eventData.game__id in this.props.navScoreboardStats.sports.games && 'points' in eventData) {
        this.props.updateGame(
          eventData.game__id,
          eventData.id,
          eventData.points
        )
      }
    })
  },

  startParityChecks() {
    log.trace('NavScoreboard.startParityChecks()')
    const self = this

    const parityChecks = {
      boxScores: window.setInterval(self.props.fetchSportsIfNeeded, 60000), // one minute
      draftGroups: window.setInterval(self.props.fetchCurrentDraftGroupsIfNeeded, 600000),  // ten minutes
    }
    self.props.fetchSportsIfNeeded()

    // if logged in, look for entries
    if (window.dfs.user.username !== '') {
      parityChecks.entries = window.setInterval(self.props.fetchEntriesIfNeeded, 60000)  // one minute
      self.props.fetchEntriesIfNeeded()
    }


    // add to the state in case we need to clearInterval in the future
    self.setState({ boxScoresIntervalFunc: parityChecks })
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
    const { username, cash_balance } = window.dfs.user
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
        <NavScoreboardUserInfo name={username} balance={cash_balance} />
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


// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    navScoreboardStats: navScoreboardSelector(state),
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    addEvent: (gameId, event) => dispatch(addEvent(gameId, event)),
    errorHandler: (exception) => dispatch(errorHandler(exception)),
    fetchCurrentDraftGroupsIfNeeded: () => dispatch(fetchCurrentDraftGroupsIfNeeded()),
    fetchEntries: () => dispatch(fetchEntries()),
    fetchEntriesIfNeeded: () => dispatch(fetchEntriesIfNeeded()),
    fetchSportsIfNeeded: () => dispatch(fetchSportsIfNeeded()),
    updateGame: (sport, gameId, teamId, points) => dispatch(updateGame(sport, gameId, teamId, points)),
  }
}

const NavScoreboardConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(NavScoreboard)

renderComponent(
  <Provider store={store}>
    <NavScoreboardConnected />
  </Provider>,
  '.cmp-nav-scoreboard'
)


export default NavScoreboard
