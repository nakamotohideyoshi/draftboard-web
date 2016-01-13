'use strict'

import React from 'react'
import {Provider, connect} from 'react-redux'
import { forEach as _forEach } from 'lodash'
import io from 'socket.io-client'
import _ from 'lodash'
import Pusher from 'pusher-js'

import errorHandler from '../../actions/live-error-handler'
import log from '../../lib/logging'
import renderComponent from '../../lib/render-component'
import store from '../../store'
import { addEvent } from '../../actions/live-game-queues'
import { fetchCurrentDraftGroupsIfNeeded } from '../../actions/current-draft-groups'
import { fetchDraftGroupStats } from '../../actions/live-draft-groups'
import { navScoreboardSelector } from '../../selectors/nav-scoreboard'
import { updateBoxScore } from '../../actions/current-box-scores'
import {fetchEntriesIfNeeded} from '../../actions/entries'
import {fetchEntries} from '../../actions/entries'
import {fetchUser} from '../../actions/user'

import NavScoreboardLogo from './nav-scoreboard-logo.jsx'
import NavScoreboardMenu from './nav-scoreboard-menu.jsx'
import NavScoreboardSlider from './nav-scoreboard-slider.jsx'
import NavScoreboardFilters from './nav-scoreboard-filters.jsx'
import NavScoreboardUserInfo from './nav-scoreboard-user-info.jsx'
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx'
import NavScoreboardGamesList from './nav-scoreboard-games-list.jsx'
import NavScoreboardLineupsList from './nav-scoreboard-lineups-list.jsx'
import NavScoreboardLoggedOutInfo from './nav-scoreboard-logged-out-info.jsx'

import {TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS} from './nav-scoreboard-const.jsx'


const NavScoreboard = React.createClass({

  propTypes: {
    boxScores: React.PropTypes.object.isRequired,
    navScoreboardStats: React.PropTypes.object.isRequired,
    fetchDraftGroupStats: React.PropTypes.func,
    fetchEntriesIfNeeded: React.PropTypes.func,
    fetchEntries: React.PropTypes.func,
    liveDraftGroups: React.PropTypes.object.isRequired,
    updateBoxScore: React.PropTypes.func,
    addEvent: React.PropTypes.func
  },

  listenToSockets() {
    log.debug('listenToSockets()')
    var self = this

    // let the live page do game score calls
    if (self.state.isLivePage === true) {
      return
    }

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
    const boxscoresChannel = pusher.subscribe(channelPrefix + 'boxscores')
    boxscoresChannel.bind('team', (eventData) => {
      if (eventData.game__id in self.props.boxScores && 'points' in eventData) {
        self.props.updateBoxScore(
          eventData.game__id,
          eventData.id,
          eventData.points
        )
      }
    })
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

      isLivePage: window.location.pathname.substring(0,6) === '/live/'
    }
  },

  startParityChecks() {
    log.debug('NavScoreboard.startParityChecks()')
    const self = this

    // loop through draft groups and get latest box scores, fp
    const boxScoresParityChecks = function() {
      log.info('NavScoreboard.boxScoresParityChecks()')

      _forEach(self.props.liveDraftGroups, (draftGroup, id) => {
        self.props.fetchDraftGroupStats(id)
      })
    }

    let parityChecks = {
      boxScores: window.setInterval(boxScoresParityChecks, 30000), // thirty seconds
      draftGroups: window.setInterval(self.props.fetchCurrentDraftGroupsIfNeeded, 600000)  // ten minutes
    }
    boxScoresParityChecks()

    // if logged in, look for entries
    if (window.dfs.user.username !== '') {
      parityChecks.entries = window.setInterval(self.props.fetchEntriesIfNeeded, 60000)  // one minute
      self.props.fetchEntriesIfNeeded()
    }


    // add to the state in case we need to clearInterval in the future
    self.setState({ 'boxScoresIntervalFunc': parityChecks })
  },

  componentWillMount() {
    let self = this

    if (this.state.user.username !== '') {
      store.dispatch(
        fetchCurrentDraftGroupsIfNeeded()
      ).catch(
        errorHandler
      ).then(() => {
        store.dispatch(
          fetchEntriesIfNeeded()
        ).then(() => {
          self.setState({isLoaded: true})

          self.listenToSockets()
          self.startParityChecks()
        }).catch(
          errorHandler
        )
      })
    } else {
      store.dispatch(
        fetchCurrentDraftGroupsIfNeeded()
      ).catch(
        errorHandler
      ).then(() => {
        self.setState({isLoaded: true})

        self.listenToSockets()
        self.startParityChecks()
      })
    }
  },

  /**
   * Handle `NavScoreboardFilters` select menu change.
   * @param {String} selectedOption Name of the selected option
   * @param {String} selectedType Type of the selected item
   * @param {String} selectedKey Key of the selected item type
   * @return {Object} options key-value pairs
   */
  handleChangeSelection(selectedOption, selectedType, selectedKey) {
    log.debug('handleChangeSelection()', selectedOption, selectedType, selectedKey)

    console.assert(typeof selectedOption === 'string')
    console.assert(typeof selectedType === 'string')
    console.assert(typeof selectedKey === 'string' || selectedKey === null)

    this.setState({selectedOption, selectedType, selectedKey})
  },

  /**
   * Get the options for `NavScoreboardFilters` select menu.
   * @return {Array} options key-value pairs
   */
  getSelectOptions() {
    let options = []

    _.forEach(this.props.navScoreboardStats.gamesByDraftGroup, (draftGroup, key) => {
      options.push({
        option: draftGroup.sport + " GAMES",
        type: TYPE_SELECT_GAMES,
        key: key
        // count: this.props.navScoreboardStats.gamesByDraftGroup[key].boxScores.length
      })
    })

    if (this.state.user.username !== '') {
      options.push({
        option: 'MY LINEUPS',
        type: TYPE_SELECT_LINEUPS,
        key: 'LINEUPS',
        count: this.props.navScoreboardStats.lineups.length
      })
    }

    return options
  },

  /**
   * Render slider contents based on selected filter.
   */
  renderSliderContent() {
    if (this.state.selectedType === TYPE_SELECT_LINEUPS) {
      return <NavScoreboardLineupsList lineups={this.props.navScoreboardStats.lineups} />
    } else if (this.state.selectedType === TYPE_SELECT_GAMES) {
      let draftGroup = this.props.navScoreboardStats.gamesByDraftGroup[this.state.selectedKey]
      return <NavScoreboardGamesList draftGroup={draftGroup} />
    } else {
      return null
    }
  },

  render() {
    const { username, cash_balance } = window.dfs.user
    let userInfo, filters, slider

    if (this.state.isLoaded === true ) {
      filters = (
        <NavScoreboardFilters
          selected={this.state.selectedOption}
          options={this.getSelectOptions()}
          onChangeSelection={this.handleChangeSelection} />
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
  }
})


// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    boxScores: state.currentBoxScores,
    navScoreboardStats: navScoreboardSelector(state),
    liveDraftGroups: state.liveDraftGroups
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    addEvent: (gameId, event) => dispatch(addEvent(gameId, event)),
    updateBoxScore: (gameId, teamId, points) => dispatch(updateBoxScore(gameId, teamId, points)),
    fetchDraftGroupStats: (draftGroupId) => dispatch(fetchDraftGroupStats(draftGroupId)),
    fetchEntriesIfNeeded: () => dispatch(fetchEntriesIfNeeded()),
    fetchEntries: () => dispatch(fetchEntries())
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
