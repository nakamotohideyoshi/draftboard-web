'use strict'

import React from 'react'
import {Provider, connect} from 'react-redux'
import { forEach as _forEach } from 'lodash'
import io from 'socket.io-client'
import _ from 'lodash'
// import Pusher from 'pusher-js'

import store from '../../store'
import log from '../../lib/logging'
import {fetchUser} from '../../actions/user'
import {fetchEntriesIfNeeded} from '../../actions/entries'
import errorHandler from '../../actions/live-error-handler'
import renderComponent from '../../lib/render-component'

import NavScoreboardLogo from './nav-scoreboard-logo.jsx'
import NavScoreboardMenu from './nav-scoreboard-menu.jsx'
import NavScoreboardSlider from './nav-scoreboard-slider.jsx'
import NavScoreboardFilters from './nav-scoreboard-filters.jsx'
import NavScoreboardUserInfo from './nav-scoreboard-user-info.jsx'
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx'
import NavScoreboardGamesList from './nav-scoreboard-games-list.jsx'
import NavScoreboardLineupsList from './nav-scoreboard-lineups-list.jsx'

import { navScoreboardSelector } from '../../selectors/nav-scoreboard'
import { updateBoxScore } from '../../actions/current-box-scores'

import {TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS} from './nav-scoreboard-const.jsx'


const NavScoreboard = React.createClass({

  propTypes: {
    boxScores: React.PropTypes.object.isRequired,
    navScoreboardStats: React.PropTypes.object.isRequired,
    updateBoxScore: React.PropTypes.func
  },

  // listenToSockets() {
  //   log.debug('listenToSockets()')
  //   var self = this

  //   let pusher = new Pusher('f23775e0c1d0da57bb4b', {
  //     encrypted: true
  //   })

  //   let channel = pusher.subscribe('nba')

  //   channel.bind('dd', (eventData) => {
  //     self.onEventSocketReceived(eventData)
  //   })
  // },

  onEventSocketReceived(eventCall) {
    log.debug('onEventReceived', eventCall.id)
    var self = this

    // if this is a statistical based call
    if ('statistics__list' in eventCall === false) {
      return false
    }

    if (eventCall.game__id in self.props.boxScores) {
      const events = eventCall.statistics__list
      // Determine if game is one we need to update in box scores. If so, then update score using points and made params
      _.forEach(events, function(event) {
        if ('made' in event && event.made === 'true') {
          self.props.updateBoxScore(eventCall.game__id, event)
        }
      })
    }
  },

  getInitialState() {
    return {
      // Selected option string. SEE: `getSelectOptions`
      selectedOption: null,

      // Selected option type. See type constants above.
      selectedType: null,

      // Selected option key. Subtype from the main type.
      // Competition from games and null for lineups.
      selectedKey: null
    }
  },

  componentWillMount() {
    let self = this

    store.dispatch(
      fetchEntriesIfNeeded()
    ).catch(
      errorHandler
    )
    // ).then(
    //   this.listenToSockets()
    // )
  },

  /**
   * Handle `NavScoreboardFilters` select menu change.
   * @param {String} selectedOption Name of the selected option
   * @param {String} selectedType Type of the selected item
   * @param {String} selectedKey Key of the selected item type
   * @return {Object} options key-value pairs
   */
  handleChangeSelection(selectedOption, selectedType, selectedKey) {
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

    options.push({
      option: 'MY LINEUPS',
      type: TYPE_SELECT_LINEUPS,
      key: null,
      count: this.props.navScoreboardStats.lineups.length
    })

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

    return (
      <div className="inner">
        <NavScoreboardMenu />
        <NavScoreboardSeparator half />
        <NavScoreboardUserInfo name={username} balance={cash_balance} />
        <NavScoreboardSeparator />
        <NavScoreboardFilters
          selected={this.state.selectedOption}
          options={this.getSelectOptions()}
          onChangeSelection={this.handleChangeSelection} />
        <NavScoreboardSlider type={this.state.selectedOption}>
          {this.renderSliderContent()}
        </NavScoreboardSlider>
        <NavScoreboardLogo />
      </div>
    )
  }
})


// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    boxScores: state.currentBoxScores,
    navScoreboardStats: navScoreboardSelector(state)
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateBoxScore: (id, event) => dispatch(updateBoxScore(id, event))
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
