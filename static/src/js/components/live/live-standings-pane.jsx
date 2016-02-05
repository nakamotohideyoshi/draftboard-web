import React from 'react'
import * as ReactRedux from 'react-redux'
import request from 'superagent'
import Cookies from 'js-cookie'
import _ from 'lodash'

import LivePMRProgressBar from './live-pmr-progress-bar'
import * as AppActions from '../../stores/app-state-store'
import { fetchLineupUsernames } from '../../actions/lineup-usernames'

/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
const LiveStandingsPane = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    owned: React.PropTypes.array.isRequired,
    lineups: React.PropTypes.object.isRequired,
    contest: React.PropTypes.object.isRequired,
    rankedLineups: React.PropTypes.array.isRequired,
    mode: React.PropTypes.object.isRequired,
    fetchLineupUsernames: React.PropTypes.func,
  },

  getInitialState() {
    return {
      page: 1,                      // Current page number starting from 1.
      perPage: 10,                  // Items per page.
      search: false,                // Whether or not search form is shown.
      searchValue: '',              // Search input value.
      currentTab: 'standings',      // Currently shown tab.
      currentPositionFilter: 'all', // Current players filter in ownership tab.
    }
  },

  componentDidMount() {
    // this.props.fetchLineupUsernames(this.props.mode.contestId)
    this.handleSearchByUsername = _.debounce(this.handleSearchByUsername, 150)
  },

  /**
   * Get list data that should be rendered in the current tab.
   * @return {Array}
   */
  getListData() {
    let data

    if (this.state.currentTab === 'standings') {
      const lineups = this.props.lineups
      const rankedLineups = this.props.rankedLineups
      data = _.map(rankedLineups, (lineupId) => lineups[lineupId])
    } else {
      data = this.props.contest.playersOwnership.all.slice()
      const filter = this.state.currentPositionFilter

      if (filter !== 'all') {
        data = _.filter(data, p => p.info.position.toLowerCase() === filter)
      }
    }

    if (this.state.searchValue !== '') {
      if (this.state.currentTab === 'standings') {
        data = data.filter(p => this.state.searchResults.indexOf(p.id) !== -1)
      } else {
        const s = this.state.searchValue
        data = data.filter(p => p.name.toLowerCase().indexOf(s.toLowerCase()) !== -1)
      }
    }

    return data
  },

  /**
   * Get the maximum page number for data in #getListData().
   * @return {Number}
   */
  getMaxPage() {
    return Math.ceil(this.getListData().length / this.state.perPage)
  },

  handleViewOwnership() {
    this.setState({
      page: 1,
      search: false,
      searchValue: '',
      searchResults: [],
      currentTab: 'ownership',
      currentPositionFilter: 'all',
    })
  },

  handleViewStandings() {
    this.setState({
      page: 1,
      search: false,
      searchValue: '',
      searchResults: [],
      currentTab: 'standings',
    })
  },

  handleViewNextPage() {
    const maxPage = this.getMaxPage()
    const page = Math.min(this.state.page + 1, maxPage)
    this.setState({ page })
  },

  handleViewPrevPage() {
    const page = Math.max(this.state.page - 1, 1)
    this.setState({ page })
  },

  /**
   * Used to view an opponent lineup. Sets up parameters to then call props.changePathAndMode()
   */
  handleViewOpponentLineup(opponentLineupId) {
    const mode = this.props.mode
    const path = `/live/lineups/${mode.myLineupId}/contests/${mode.contestId}/opponents/${opponentLineupId}/`
    const changedFields = {
      opponentLineupId,
    }

    this.props.changePathAndMode(path, changedFields)
    AppActions.toggleLiveRightPane('appstate--live-standings-pane--open')
  },

  handleSetPositionFilter(currentPositionFilter) {
    this.setState({ currentPositionFilter, page: 1 })
  },

  handleToggleSearch() {
    this.setState({
      search: !this.state.search,
      searchValue: '',
    })

    if (this.refs.search) {
      this.refs.search.focus()
    }
  },

  handleSearchTermChanged() {
    this.setState({ searchValue: this.refs.search.value })

    if (this.state.currentTab === 'standings') {
      this.handleSearchByUsername();
    }
  },

  handleSearchByUsername() {
    const params = {
      contest_id: this.props.mode.contestId,
      search_str: this.state.searchValue,
    }

    // TODO: report errors
    return request
      .post('/api/lineup/usernames/')
      .send(params)
      .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
      .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
      .set('Accept', 'application/json')
      .end((err, res) => {
        if (!err) {
          let data;
          try {
            data = JSON.parse(res.text);
          } catch (e) {
            data = [];
          }

          this.setState({ searchResults: data.map((l) => l.id) });
        } else {
          this.setState({ searchResults: [] });
        }
      })
  },

  handleSearchInputBlur() {
    if (this.refs.search.value === '') {
      this.setState({ search: false })
    }
  },

  handleClosePane() {
    AppActions.removeClass('appstate--live-standings-pane--open')
  },

  renderHeader() {
    return (
      <div className="live-standings-pane__header">
        <div
          className={`title${(this.state.currentTab === 'standings' ? ' active' : '')}`}
          onClick={this.handleViewStandings}
        >
          Standings
          <div className="border"></div>
        </div>
        <div
          className={`title${(this.state.currentTab === 'ownership' ? ' active' : '')}`}
          onClick={this.handleViewOwnership}
        >
          % Owned
          <div className="border"></div>
        </div>
        <div className={`search${(this.state.search ? ' active' : '')}`}>
          <div className="icon" onClick={this.handleToggleSearch}></div>
          <input type="text"
            ref="search"
            value={this.state.searchValue}
            onBlur={this.handleSearchInputBlur}
            onChange={this.handleSearchTermChanged}
          />
        </div>
      </div>
    )
  },

  renderPages() {
    const { page } = this.state
    const maxPage = this.getMaxPage()

    const pages = (new Array(maxPage)).join(',').split(',').map((a, i) =>
      <div key={i} className={`page${((page - 1) === i ? ' selected' : '')}`}></div>
    )

    // if only one page, then don't show paginator
    if (maxPage === 1) {
      return null
    }

    return (
      <div className="live-standings-pane__pages">
        <div
          className="arrow-left"
          onClick={this.handleViewPrevPage}
        >
          <span>&lt;</span>
        </div>
        {pages}
        <div
          className="arrow-right"
          onClick={this.handleViewNextPage}
        >
          <span>&gt;</span>
        </div>
      </div>
    )
  },

  renderStandings() {
    const { page, perPage } = this.state
    let data = this.getListData()
    data = data.slice(
      (page - 1) * perPage,
      Math.min(page * perPage, data.length)
    )
    const mode = this.props.mode

    const standings = data.map((lineup) => {
      let className = 'lineup'
      let pmr = (
        <LivePMRProgressBar
          decimalRemaining={lineup.decimalRemaining}
          strokeWidth={2}
          backgroundHex="46495e"
          hexStart="ffffff"
          hexEnd="ffffff"
          svgWidth={50}
        />
      )
      let overlay = (
        <div
          className="overlay"
          onClick={this.handleViewOpponentLineup.bind(this, lineup.id)}
        >
          Compare Lineup
        </div>
      )

      if (mode.myLineupId === lineup.id) {
        overlay = ''
        className += ' lineup--mine'
        pmr = (
          <LivePMRProgressBar
            decimalRemaining={lineup.decimalRemaining}
            strokeWidth={2}
            backgroundHex="46495e"
            hexStart="34B4CC"
            hexEnd="2871AC"
            svgWidth={50}
          />
        )
      }
      let username = ''
      if (lineup.hasOwnProperty('user') && lineup.user.hasOwnProperty('username')) {
        username = lineup.user.username
      }
      return (
        <div key={lineup.id} className={ className }>
          <div className="lineup--place">{lineup.rank}</div>
          { pmr }
          <div className="lineup--score-name">{username}</div>
          <div className="lineup--score-points"><b>{lineup.points}</b><span>Pts</span></div>
          <div className="lineup--score-earnings">${lineup.potentialEarnings}</div>
          { overlay }
        </div>
      )
    })

    return (
      <div className="standings-list">
        {standings}
      </div>
    )
  },

  renderPlayers() {
    const { page, perPage } = this.state
    let data = this.getListData()
    data = data.slice(
      (page - 1) * perPage,
      Math.min(page * perPage, data.length)
    )

    const players = data.map((player) => (
      <div key={player.id} className="player">
        <div className="player--position">{player.info.position}</div>
        <div className="player--pmr-photo">
          <LivePMRProgressBar
            decimalRemaining={player.stats.decimalRemaining}
            strokeWidth={3}
            backgroundHex="46495e"
            hexStart="ffffff"
            hexEnd="ffffff"
            svgWidth={50}
          />
          <div className="avatar" />
        </div>
        <div className="player--name">
          {player.info.name} <div className="team">{player.info.team_alias}</div>
        </div>
        <div className="player--points"><b>{player.stats.fp}</b><span>Pts</span></div>
        <div className="player--progress">{player.ownershipPercent}%</div>
      </div>
    ))

    return (
      <div className="ownership-list">
        {players}
      </div>
    )
  },

  renderStandingsTab() {
    if (this.state.currentTab !== 'standings') return null

    // wait for usernames
    if (this.props.contest.hasLineupsUsernames === false) return null

    return (
      <div className="inner">
        {this.renderHeader()}
        {this.renderStandings()}
        {this.renderPages()}
      </div>
    )
  },

  renderOwnershipTab() {
    if (this.state.currentTab !== 'ownership') return null

    const filters = ['all', 'pg', 'sg', 'sf', 'pf', 'c'].map((f) => {
      let className = `position-filter ${f}`
      if (f === this.state.currentPositionFilter) className += ' active'

      return (
          <div key={f}
            className={className}
            onClick={this.handleSetPositionFilter.bind(this, f)}
          >
          {f}
        </div>
      )
    })

    let onClick = ''
    if (this.props.mode.opponentLineupId !== 1) {
      onClick = this.handleViewOpponentLineup.bind(this, 1)
    }

    return (
      <div className="inner">
        {this.renderHeader()}
        <div className="position-filter">{filters}</div>
        <div className="watch-live" onClick={onClick}>
          Watch top 8 owned players live
        </div>
        {this.renderPlayers()}
        {this.renderPages()}
      </div>
    )
  },

  render() {
    const classNames = `live-pane live-pane--right live-standings-pane live-standings-pane--${this.state.currentTab}`

    return (
      <div className={classNames}>
        <div className="live-pane__close" onClick={this.handleClosePane}></div>
        {this.renderStandingsTab()}
        {this.renderOwnershipTab()}
      </div>
    )
  },
})


// Redux integration
const { connect } = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps() {
  // TODO:
  return {
    owned: [
      {
        id: 1,
        name: 'Kobe Bryant',
        team: 'LAL',
        points: 72,
        position: 'pg',
        iamge: '',
        progress: 0.99,
      },
      {
        id: 2,
        name: 'Kobe Bryant',
        team: 'LAL',
        points: 12,
        position: 'c',
        iamge: '',
        progress: 0.3,
      },
    ],
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchLineupUsernames: (id) => dispatch(fetchLineupUsernames(id)),
  }
}

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveStandingsPane)
