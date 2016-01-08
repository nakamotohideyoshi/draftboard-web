import React from 'react'
import {Provider, connect} from 'react-redux';
import store from '../../store'
import renderComponent from '../../lib/render-component';
import PrizeStructure from './prize-structure.jsx'
import GamesList from './games-list.jsx'
import EntrantList from './entrant-list.jsx'
import {enterContest, setFocusedContest, fetchContestEntrantsIfNeeded}
  from '../../actions/upcoming-contests-actions.js'
import * as AppActions from '../../stores/app-state-store.js'
import { Router, Route } from 'react-router'
import {updatePath, syncReduxAndRouter} from 'redux-simple-router'
import createBrowserHistory from 'history/lib/createBrowserHistory'
import CountdownClock from '../site/countdown-clock.jsx'
import {fetchDraftGroupBoxScoresIfNeeded} from '../../actions/draft-group-actions.js'
import {fetchTeamsIfNeeded} from '../../actions/sports.js'

const history = createBrowserHistory()
syncReduxAndRouter(history, store)


/**
 * Renders a slideout pane with details of the selected contest.
 */
var ContestListDetail = React.createClass({

  propTypes: {
    boxScores: React.PropTypes.object,
    contest: React.PropTypes.object,
    enterContest: React.PropTypes.func,
    entrants: React.PropTypes.array,
    fetchContestEntrantsIfNeeded: React.PropTypes.func,
    fetchDraftGroupBoxScoresIfNeeded: React.PropTypes.func,
    fetchTeamsIfNeeded: React.PropTypes.func,
    focusedContestId: React.PropTypes.oneOfType([React.PropTypes.number, React.PropTypes.string]),
    focusedLineupId: React.PropTypes.number,
    params: React.PropTypes.object,
    prizeStructure: React.PropTypes.object,
    setFocusedContest: React.PropTypes.func,
    teams: React.PropTypes.object
  },


  /**
   * When we get new props, check to see if the focusedContestId is the same as the id in the URL.
   * if it isn't, set what's in the URL as the focused contest and open the side panel to view it.
   */
  componentWillReceiveProps: function(nextProps) {
    // A new contest has been focused. Fetch all of it's required data.
    if (nextProps.params.contestId && this.props.focusedContestId != nextProps.params.contestId) {
      AppActions.openPane();
      // This is what "monitors" for URL changes.
      this.props.setFocusedContest(nextProps.params.contestId)
      this.props.fetchDraftGroupBoxScoresIfNeeded(nextProps.params.contestId)
      this.props.fetchContestEntrantsIfNeeded(nextProps.params.contestId)
    }

    // If we don't have team names (we problably do), fetch them.
    if (nextProps.params.contest && nextProps.params.contest.hasOwnProperty('sport')) {
      this.props.fetchTeamsIfNeeded(nextProps.params.contest.sport)
    }
  },


  getInitialState: function() {
    return {
      activeTab: 'prizes'
    }
  },

  // Enter the currently focused lineup into a contest.
  handleEnterContest: function(contestId) {
    this.props.enterContest(contestId, this.props.focusedLineupId)
  },


  // Get the content of the selected tab.
  getActiveTab: function() {
    switch (this.state.activeTab) {
      case 'prizes':
        return (<PrizeStructure structure={this.props.prizeStructure} />)

      case 'scoring':
        return 'scoring tab'

      case 'games':
        if (this.props.boxScores.hasOwnProperty(this.props.contest.id)) {
          return (
            <GamesList
              boxScores={this.props.boxScores[this.props.contest.id]}
              teams={this.props.teams[this.props.contest.sport]}
            />
            )
        }

        return 'no boxscore info'

      case 'entries':
        return (
          <EntrantList entrants={this.props.entrants} />
        )

      default:
        return ('Select a tab')
    }
  },


  // When a tab is clicked, tell the state to show it'scontent.
  handleTabClick: function(tabName) {
    this.setState({'activeTab': tabName})
  },


  // I know making these their own components would be more 'react', but I don't want to deal with
  // the hassle right now.
  getTabNav: function() {
    const tabs = [
      {title: 'Payout', tab: 'prizes'},
      {title: 'Scoring', tab: 'scoring'},
      {title: 'Games', tab: 'games'},
      {title: 'Entries', tab: 'entries'}
    ]

    return tabs.map(function(tab) {
      let classes = ''

      if (this.state.activeTab === tab.tab) {
        classes = 'active'
      }

      return (
        <li key={tab.tab} className={classes} onClick={this.handleTabClick.bind(this, tab.tab)}>{tab.title}</li>
      )
    }.bind(this))
  },


  getContest: function() {
    if(this.props.contest) {
      let tabNav = this.getTabNav()

      return (
        <div className="pane--contest-detail">
          <div className="pane-upper">
            <div className="header">
              <div className="header__content">
                <div className="title">{this.props.contest.name}</div>
                <div className="header__info">
                  <div>
                    <div className="info-title">Live In</div>
                    <span><CountdownClock time={this.props.contest.start} /></span>
                  </div>
                </div>

                <div className="header__extra-info">
                  <div className="m badge">M</div>
                  <div className="g badge">G</div>
                </div>

                <div className="header__fee-prizes-pool">
                  <div><span className="info-title">Prize</span><div>${this.props.contest.prize_pool.toFixed(2)}</div></div>
                  <div><span className="info-title">Fee</span><div>${this.props.contest.buyin.toFixed(2)}</div></div>
                  <div>
                    <span className="info-title">Entrants</span>
                    <div>{this.props.contest.current_entries} / {this.props.contest.entries}</div>
                  </div>
                </div>

                <div
                  className="button button--gradient button--medium btn-enter-contest"
                  onClick={this.handleEnterContest.bind(null, this.props.focusedLineupId)}
                >
                  Enter Contest
                </div>
              </div>
            </div>
          </div>

          <div colSpan="9" className="pane-lower">
            <ul className="tab-nav">{tabNav}</ul>
            <div className="tab-content">{this.getActiveTab()}</div>
          </div>

        </div>
      )
    }
    else {
      return (
        <div>Select a Contest</div>
      )
    }
  },

  render: function() {
    let contestDetail = this.getContest();

    return (
      <div className="cmp-contest-list__detail">
        {contestDetail}
      </div>
    )
  }

})



function mapStateToProps(state) {
  // TODO: put this in a reusable selector.
  let contest = state.upcomingContests.allContests[state.upcomingContests.focusedContestId]
  let prizeStructure = null
  let entrants = []

  if (contest && contest.hasOwnProperty('prize_structure')) {
    prizeStructure = state.prizes[contest.prize_structure]
  }

  if (contest && state.upcomingContests.entrants.hasOwnProperty(contest.id)) {
    entrants = state.upcomingContests.entrants[contest.id]
  }

  return {
    contest,
    focusedContestId: state.upcomingContests.focusedContestId,
    prizeStructure,
    focusedLineupId: state.upcomingLineups.focusedLineupId,
    boxScores: state.upcomingDraftGroups.boxScores,
    teams: state.sports,
    entrants
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    enterContest: (contestId, lineupId) => dispatch(enterContest(contestId, lineupId)),
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId)),
    fetchDraftGroupBoxScoresIfNeeded: (draftGroupId) => dispatch(fetchDraftGroupBoxScoresIfNeeded(draftGroupId)),
    fetchContestEntrantsIfNeeded: (contestId) => dispatch(fetchContestEntrantsIfNeeded(contestId))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var ContestListDetailConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(ContestListDetail);

renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/lobby/" component={ContestListDetailConnected} />
      <Route path="/lobby/:contestId/" component={ContestListDetailConnected} />
    </Router>
  </Provider>,
  '.cmp-contest-list-detail'
);


module.exports = ContestListDetailConnected
