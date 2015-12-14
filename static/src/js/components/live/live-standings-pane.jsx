import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import { updatePath } from 'redux-simple-router'
import { vsprintf } from 'sprintf-js'

import LiveStandingsPaneCircle from './live-standings-pane-circle'
import * as AppActions from '../../stores/app-state-store'
import { updateLiveMode } from '../../actions/live'
import { fetchLineupUsernames } from '../../actions/lineup-usernames'
import { fetchContestIfNeeded } from '../../actions/live-contests'
import { liveSelector } from '../../selectors/live'
import { liveContestsStatsSelector } from '../../selectors/live-contests'
import store from '../../store'


/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
export const LiveStandingsPane = React.createClass({

  propTypes: {
    contestId: React.PropTypes.number.isRequired,
    owned: React.PropTypes.array.isRequired,
    lineups: React.PropTypes.array.isRequired,
    mode: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func,
    fetchLineupUsernames: React.PropTypes.func
  },

  getInitialState() {
    return {
      page: 1,                     // Current page number starting from 1.
      perPage: 10,                 // Items per page.
      search: false,               // Whether or not search form is shown.
      searchValue: '',             // Search input value.
      currentTab: 'standings',     // Currently shown tab.
      currentPositionFilter: 'all' // Current players filter in ownership tab.
    }
  },

  componentDidMount() {
    this.props.fetchLineupUsernames(this.props.contestId)
  },

  /**
   * Get list data that should be rendered in the current tab.
   * @return {Array}
   */
  getListData() {
    let data

    if (this.state.currentTab === 'standings') {
      data =  this.props.lineups
    } else {
      data = this.props.owned
      let filter = this.state.currentPositionFilter

      if (filter !== 'all') {
        data = data.filter(p => p.position === filter)
      }
    }

    if (this.state.searchValue !== '') {
      const s = this.state.searchValue
      data = data.filter(p => p.name.toLowerCase().indexOf(s.toLowerCase()) !== -1)
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
      currentTab: 'ownership',
      currentPositionFilter: 'all'
    })
  },

  handleViewStandings() {
    this.setState({ currentTab: 'standings', page: 1 })
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

  handleViewOpponentLineup(lineup) {
    const mode = this.props.mode
    const opponentLineupId = lineup.id

    this.props.updatePath(vsprintf('/live/lineups/%d/contests/%d/opponents/%d/', [
      mode.myLineupId,
      mode.contestId,
      opponentLineupId
    ]))
    this.props.updateLiveMode({
      opponentLineupId: opponentLineupId
    })
  },

  handleSetPositionFilter(currentPositionFilter) {
    this.setState({currentPositionFilter, page: 1})
  },

  handleWatchTopOwnedPlayers() {
    // TODO:
  },

  handleToggleSearch() {
    this.setState({
      search: !this.state.search,
      searchValue: ''
    })

    if (this.refs.search) {
      this.refs.search.focus()
    }
  },

  handleSearchTermChanged() {
    this.setState({searchValue: this.refs.search.value})
  },

  handleSearchInputBlur() {
    if (this.refs.search.value === '') {
      this.setState({search: false})
    }
  },

  handleClosePane() {
    AppActions.removeClass('appstate--live-standings-pane--open')
  },

  renderHeader() {
    return (
      <div className="live-standings-pane__header">
        <div className={'title' + (this.state.currentTab === 'standings' ? ' active' : '')}
             onClick={this.handleViewStandings}>
          Standings
          <div className="border"></div>
        </div>
        <div className={'title' + (this.state.currentTab === 'ownership' ? ' active' : '')}
             onClick={this.handleViewOwnership}>
          % Owned
          <div className="border"></div>
        </div>
        <div className={'search' + (this.state.search ? ' active' : '')}>
          <div className="icon" onClick={this.handleToggleSearch}></div>
          <input type="text"
                 ref="search"
                 value={this.state.searchValue}
                 onBlur={this.handleSearchInputBlur}
                 onChange={this.handleSearchTermChanged} />
        </div>
      </div>
    )
  },

  renderPages() {
    const {page} = this.state
    const maxPage = this.getMaxPage()

    const pages = (new Array(maxPage)).join(',').split(',').map((_, i) => {
      return <div key={i} className={'page' + ((page - 1) === i ? ' selected' : '')}></div>
    })

    return (
      <div className="live-standings-pane__pages">
        <div className="arrow-left"
             onClick={this.handleViewPrevPage}>
          <span>&lt;</span>
        </div>
        {pages}
        <div className="arrow-right"
             onClick={this.handleViewNextPage}>
          <span>&gt;</span>
        </div>
      </div>
    )
  },

  renderStandings() {
    const {page, perPage} = this.state
    let data = this.getListData()
    data = data.slice(
      (page - 1) * perPage,
      Math.min(page * perPage, data.length)
    )

    const standings = data.map((lineup, i) => {
      return (
        <div key={lineup.id} className="lineup">
          <div className="lineup--place">{lineup.rank}</div>
          <LiveStandingsPaneCircle progress={lineup.pmr} />
          <div className="lineup--score-name">{lineup.name}</div>
          <div className="lineup--score-points"><b>{lineup.points}</b><span>Pts</span></div>
          <div className="lineup--score-earnings">{lineup.earnings}</div>
          <div className="overlay"
               onClick={this.handleViewOpponentLineup.bind(this, lineup)}>
            Compare Lineup
          </div>
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
    const {page, perPage} = this.state
    let data = this.getListData()
    data = data.slice(
      (page - 1) * perPage,
      Math.min(page * perPage, data.length)
    )

    const players = data.map((player, i) => {
      return (
        <div key={player.id} className="player">
          <div className="player--position">{player.position}</div>
          <LiveStandingsPaneCircle progress={player.progress} />
          <div className="avatar"
               style={{
                 // TODO:
                 // backgroundImage: "url('" + player.image + "')"
               }}>
          </div>
          <div className="player--name">
            {player.name} <div className="team">{player.team}</div>
          </div>
          <div className="player--points"><b>{player.points}</b><span>Pts</span></div>
          <div className="player--progress">{player.progress}</div>
        </div>
      )
    })

    return (
      <div className="ownership-list">
        {players}
      </div>
    )
  },

  renderStandingsTab() {
    if (this.state.currentTab !== 'standings') return null

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
               onClick={this.handleSetPositionFilter.bind(this, f)}>
          {f}
        </div>
      )
    })

    return (
      <div className="inner">
        {this.renderHeader()}
        <div className="position-filter">{filters}</div>
        <div className="watch-live" onClick={this.handleWatchTopOwnedPlayers}>
          Watch top 8 owned players live
        </div>
        {this.renderPlayers()}
        {this.renderPages()}
      </div>
    )
  },

  render() {
    let classNames = 'live-pane live-pane--right live-standings-pane live-standings-pane--' + this.state.currentTab

    return (
      <div className={classNames}>
        <div className="live-pane__close" onClick={this.handleClosePane}></div>
        {this.renderStandingsTab()}
        {this.renderOwnershipTab()}
      </div>
    )
  }
})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  const contestId = 2
  const contestStats = liveContestsStatsSelector(state)
  const lineupUsernames  = (state.lineupUsernames[contestId] || {}).lineups || {}

  let lineups = (contestStats[contestId] || {}).rankedLineups || []
  lineups = lineups.map((l) => {
    return Object.assign({
      name: lineupUsernames[l.id] || '-',
      pmr: 10, // TODO:
      earnings: '$' + l.potentialEarnings
    }, l)
  })

  // TODO:
  return {
    contestId,
    owned: [
      {
        id: 1,
        name: 'Kobe Bryant',
        team: 'LAL',
        points: 72,
        position: 'pg',
        iamge: '',
        progress: 100
      },
      {
        id: 2,
        name: 'Kobe Bryant',
        team: 'LAL',
        points: 12,
        position: 'c',
        iamge: '',
        progress: 30
      }
    ],
    lineups
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (newMode) => dispatch(updateLiveMode(newMode)),
    updatePath: (path) => dispatch(updatePath(path)),
    fetchContestIfNeeded: (id) => dispatch(fetchContestIfNeeded(id)),
    fetchLineupUsernames: (id) => dispatch(fetchLineupUsernames(id))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveStandingsPaneConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveStandingsPane)

// Render the component.
renderComponent(
  <Provider store={store}>
    <LiveStandingsPaneConnected />
  </Provider>,
  '.live-standings-pane'
)

export default LiveStandingsPaneConnected
