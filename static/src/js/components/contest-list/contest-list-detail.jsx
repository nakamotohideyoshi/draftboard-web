import React from 'react'
import {Provider, connect} from 'react-redux';
import store from '../../store'
import renderComponent from '../../lib/render-component';
import PrizeStructure from './prize-structure.jsx'
import GamesList from './games-list.jsx'
import EntrantList from './entrant-list.jsx'
import EnterContestButton from './enter-contest-button.jsx'
import {enterContest, setFocusedContest, fetchContestEntrantsIfNeeded}
  from '../../actions/upcoming-contests-actions.js'
import * as AppActions from '../../stores/app-state-store.js'
import { Router, Route } from 'react-router'
import {syncReduxAndRouter} from 'redux-simple-router'
import createBrowserHistory from 'history/lib/createBrowserHistory'
import CountdownClock from '../site/countdown-clock.jsx'
import {fetchDraftGroupBoxScoresIfNeeded} from '../../actions/upcoming-draft-groups-actions.js'
import {focusedContestInfoSelector, focusedLineupSelector} from '../../selectors/lobby-selectors.js'
import {upcomingLineupsInfo} from '../../selectors/upcoming-lineups-info.js'

const history = createBrowserHistory()
syncReduxAndRouter(history, store)


/**
 * Renders a slideout pane with details of the selected contest.
 */
var ContestListDetail = React.createClass({

  propTypes: {
    boxScores: React.PropTypes.object,
    contestInfo: React.PropTypes.object,
    enterContest: React.PropTypes.func,
    fetchContestEntrantsIfNeeded: React.PropTypes.func,
    fetchDraftGroupBoxScoresIfNeeded: React.PropTypes.func,
    fetchTeamsIfNeeded: React.PropTypes.func,
    focusedLineup: React.PropTypes.object,
    params: React.PropTypes.object,
    setFocusedContest: React.PropTypes.func,
    teams: React.PropTypes.object,
    lineupsInfo: React.PropTypes.object
  },


  /**
   * When we get new props, check to see if the focusedContestId is the same as the id in the URL.
   * if it isn't, set what's in the URL as the focused contest and open the side panel to view it.
   */
  componentWillReceiveProps: function(nextProps) {
    // A new contest has been focused. Fetch all of it's required data.
    if (nextProps.params.contestId && this.props.contestInfo.contest.id != nextProps.params.contestId) {
      AppActions.openPane();
      // // This is what "monitors" for URL changes.
      this.props.setFocusedContest(nextProps.params.contestId)
      this.props.fetchContestEntrantsIfNeeded(nextProps.params.contestId)

      // If we've got the selected contest, use it's draft_group id to get the boxscores.
      if (this.props.contestInfo.contest.hasOwnProperty('draft_group')) {
        this.props.fetchDraftGroupBoxScoresIfNeeded(this.props.contestInfo.contest.draft_group)
      }
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


  // Get the content of the selected tab.
  getActiveTab: function() {
    switch (this.state.activeTab) {
      case 'prizes':
        return (<PrizeStructure structure={this.props.contestInfo.prizeStructure} />)

      case 'games':
        if (this.props.boxScores.hasOwnProperty(this.props.contestInfo.contest.id)) {
          return (
            <GamesList
              boxScores={this.props.boxScores[this.props.contestInfo.contest.id]}
              teams={this.props.teams[this.props.contestInfo.contest.sport]}
            />
            )
        }

        return 'no boxscore info'

      case 'entries':
        return (
          <EntrantList entrants={this.props.contestInfo.entrants} />
        )

      default:
        return ('Select a tab')
    }
  },


  // When a tab is clicked, tell the state to show it'scontent.
  handleTabClick: function(tabName) {
    this.setState({'activeTab': tabName})
  },


  // Enter the currently focused lineup into a contest.
  // TODO: this is copypasta from loby-contests.jsx. THis should really be a child copmponent of
  // that but I kinda screwed up a long time ago. fix this someday.
  handleEnterContest: function(contest) {
    this.enterContest(contest.id);
  },

  enterContest: function(contestId) {
    this.props.enterContest(contestId, this.props.focusedLineup.id);
  },


  // I know making these their own components would be more 'react', but I don't want to deal with
  // the hassle right now.
  getTabNav: function() {
    const tabs = [
      {title: 'Payout', tab: 'prizes'},
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
    if(this.props.contestInfo.contest.id) {
      let tabNav = this.getTabNav()

      return (
        <div className="pane--contest-detail">
          <div className="pane-upper">
            <div className="header">
              <div className="header__content">
                <div className="title">{this.props.contestInfo.contest.name}</div>
                <div className="header__info">
                  <div>
                    <div className="info-title">Live In</div>
                    <span><CountdownClock time={this.props.contestInfo.contest.start} /></span>
                  </div>
                </div>

                <div className="header__extra-info">
                  <div className="m badge">M</div>
                  <div className="g badge">G</div>
                </div>

                <div className="header__fee-prizes-pool">
                  <div><span className="info-title">Prize</span><div>${this.props.contestInfo.contest.prize_pool.toFixed(2)}</div></div>
                  <div><span className="info-title">Fee</span><div>${this.props.contestInfo.contest.buyin.toFixed(2)}</div></div>
                  <div>
                    <span className="info-title">Entrants</span>
                    <div>{this.props.contestInfo.contest.current_entries} / {this.props.contestInfo.contest.entries}</div>
                  </div>
                </div>

                <div className="btn-enter-contest">
                  <EnterContestButton
                    lineup={this.props.focusedLineup}
                    contest={this.props.contestInfo.contest}
                    lineupsInfo={this.props.lineupsInfo}
                    onEnterClick={this.handleEnterContest}
                    onEnterSuccess={this.close}
                    buttonText= {{
                      draft: 'Draft a Team',
                      started: 'Contest Has Started',
                      enter: 'Enter Contest',
                      entering: 'Entering...',
                      entered: 'Entered'
                    }}
                  />
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
  return {
    contestInfo: focusedContestInfoSelector(state),
    focusedLineup: focusedLineupSelector(state),
    boxScores: state.upcomingDraftGroups.boxScores,
    teams: state.sports,
    lineupsInfo: upcomingLineupsInfo(state)
  }
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
