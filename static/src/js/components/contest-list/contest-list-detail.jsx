import React from 'react';
import { Provider, connect } from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import PrizeStructure from './prize-structure.jsx';
import GamesList from './games-list.jsx';
import EntryList from './entry-list.jsx';
import EnterContestButton from './enter-contest-button.jsx';
import ScoringInfo from './scoring-info';
import { enterContest, setFocusedContest, removeContestPoolEntry }
  from '../../actions/contest-pool-actions';
import * as AppActions from '../../stores/app-state-store';
import { humanizeCurrency } from '../../lib/utils/currency';
import { push as routerPush } from 'react-router-redux';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import CountdownClock from '../site/countdown-clock.jsx';
import { fetchDraftGroupBoxScoresIfNeeded } from '../../actions/upcoming-draft-groups-actions';
import { focusedContestInfoSelector, focusedLineupSelector, entrySkillLevelsSelector }
  from '../../selectors/lobby-selectors';
import { upcomingLineupsInfo } from '../../selectors/upcoming-lineups-info';
import PubSub from 'pubsub-js';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    allContests: state.contestPools.allContests,
    isFetchingContestPools: state.contestPools.isFetchingContestPools,
    focusedContestInfo: focusedContestInfoSelector(state),
    focusedLineup: focusedLineupSelector(state),
    focusedContestId: state.contestPools.focusedContestId,
    boxScores: state.upcomingDraftGroups.boxScores,
    teams: state.sports,
    lineupsInfo: upcomingLineupsInfo(state),
    entrySkillLevels: entrySkillLevelsSelector(state),
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    enterContest: (contestId, lineupId) => dispatch(enterContest(contestId, lineupId)),
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId)),
    fetchDraftGroupBoxScoresIfNeeded: (draftGroupId) => dispatch(fetchDraftGroupBoxScoresIfNeeded(draftGroupId)),
    removeContestPoolEntry: (entryId) => dispatch(removeContestPoolEntry(entryId)),
    routerPush: (path) => dispatch(routerPush(path)),
  };
}


/**
 * Renders a slideout pane with details of the selected contest.
 */
const ContestListDetail = React.createClass({

  propTypes: {
    allContests: React.PropTypes.object,
    boxScores: React.PropTypes.object,
    focusedContestInfo: React.PropTypes.object,
    enterContest: React.PropTypes.func,
    fetchDraftGroupBoxScoresIfNeeded: React.PropTypes.func,
    fetchTeamsIfNeeded: React.PropTypes.func,
    focusedContestId: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.number,
    ]),
    focusedLineup: React.PropTypes.object,
    isFetchingContestPools: React.PropTypes.bool.isRequired,
    params: React.PropTypes.object,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
    setFocusedContest: React.PropTypes.func,
    teams: React.PropTypes.object,
    lineupsInfo: React.PropTypes.object,
    routerPush: React.PropTypes.func,
    entrySkillLevels: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    return {
      activeTab: 'my_entries',
    };
  },


  componentWillMount() {
    PubSub.subscribe('pane.close', this.stripContestFromUrl);
  },


  /**
   * When we get new props, check to see if the focusedContestId is the same as the id in the URL.
   * if it isn't, set what's in the URL as the focused contest and open the side panel to view it.
   */
  componentWillReceiveProps(nextProps) {
    // A new contest has been focused. Fetch all of it's required data.
    if (
        nextProps.params.contestId &&
        nextProps.focusedContestInfo.contest.id !== nextProps.params.contestId
      ) {
      AppActions.openPane();
      // This is what "monitors" for URL changes.
      // If our current url prop for contestId does not match the focousedContest in the state,
      // set the  new one as focused.
      if (this.props.focusedContestId !== nextProps.params.contestId) {
        this.props.setFocusedContest(nextProps.params.contestId);
      }
    }

    // If we've got the selected contest, use it's draft_group id to get the boxscores.
    if (nextProps.focusedContestInfo.contest.draft_group) {
      this.props.fetchDraftGroupBoxScoresIfNeeded(nextProps.focusedContestInfo.contest.draft_group);
    }

    // If we don't have team names (we problably do), fetch them.
    if (nextProps.params.contest && nextProps.params.contest.hasOwnProperty('sport')) {
      this.props.fetchTeamsIfNeeded(nextProps.params.contest.sport);
    }
  },


  // Get the content of the selected tab.
  getActiveTab() {
    switch (this.state.activeTab) {
      case 'prizes':
        return (<PrizeStructure structure={this.props.focusedContestInfo.contest.prize_structure} />);

      case 'games': {
        if (this.props.focusedContestInfo.boxScores) {
          return (
            <GamesList
              boxScores={this.props.focusedContestInfo.boxScores}
              teams={this.props.teams[this.props.focusedContestInfo.contest.sport]}
            />
          );
        }

        return 'No boxscore info';
      }

      case 'my_entries': {
        return (
          <EntryList
            entries={this.props.focusedContestInfo.contest.entryInfo}
            contestPoolInfo={this.props.focusedContestInfo}
            removeContestPoolEntry={this.props.removeContestPoolEntry}
          />
        );
      }

      case 'scoring': {
        return (
          <ScoringInfo sport={this.props.focusedContestInfo.contest.sport} />
        );
      }

      default: {
        return ('Select a tab');
      }
    }
  },


  // I know making these their own components would be more 'react', but I don't want to deal with
  // the hassle right now.
  getTabNav() {
    const tabs = [
      { title: 'My Entries', tab: 'my_entries' },
      { title: 'Entries', tab: 'entries' },
      { title: 'Prizes', tab: 'prizes' },
      { title: 'Games', tab: 'games' },
      { title: 'Scoring', tab: 'scoring' },
    ];

    return tabs.map((tab) => {
      let classes = '';

      if (this.state.activeTab === tab.tab) {
        classes = 'active';
      }

      return (
        <li
          key={tab.tab}
          className={classes}
          onClick={this.handleTabClick.bind(this, tab.tab)}
        >
          {tab.title}
        </li>
      );
    });
  },


  getEnterContestButton() {
    let enteredText = 'Enter Again';

    if (this.props.focusedLineup) {
      enteredText = `Enter '${this.props.focusedLineup.name}' Again`;
    }

    return (
      <EnterContestButton
        lineup={this.props.focusedLineup}
        contest={this.props.focusedContestInfo.contest}
        lineupsInfo={this.props.lineupsInfo}
        onEnterClick={this.handleEnterContest}
        onEnterSuccess={this.close}
        buttonText= {{
          draft: 'Draft a Team',
          started: 'Contest Has Started',
          enter: 'Enter Contest',
          entering: 'Entering...',
          entered: enteredText,
          maxEntered: 'Max Entries Reached',
        }}
        buttonClasses= {{
          default: 'button--med button--med-len button--gradient',
          contestEntered: 'button--med button--med-len button--gradient',
          pending: 'button--med button--med-len button--gradient',
          contestHasStarted: 'button--med button--med-len button--gradient',
          maxEntered: 'button--med button--med-len button--gradient',
        }}
        entrySkillLevels = {this.props.entrySkillLevels}
      />
    );
  },


  getContest() {
    if (this.props.focusedContestInfo.contest.id) {
      const tabNav = this.getTabNav();


      return (
        <div className="pane--contest-detail">
          <div
            onClick={this.closePane}
            className="pane__close"
          ></div>
          <div className="pane-upper">
            <div className="header">
              <div className="header__content">
                <div className="title">{this.props.focusedContestInfo.contest.name}</div>
                <div className="header__info">
                  <div>
                    <span>
                      <CountdownClock
                        time={this.props.focusedContestInfo.contest.start}
                        timePassedDisplay="Live"
                      />
                    </span>
                    <div className="clock-labels"><span>H</span> <span>M</span> <span>S</span></div>
                  </div>
                </div>

                <div className="header__fee-prizes-pool">
                  <div>
                    <span className="info-title">Prize Pool</span>
                    <div>{humanizeCurrency(this.props.focusedContestInfo.contest.prize_pool)}</div>
                  </div>
                  <div>
                    <span className="info-title">Entries</span>
                    <div>
                      {this.props.focusedContestInfo.contest.current_entries} /&nbsp;
                      {this.props.focusedContestInfo.contest.max_entries}
                    </div>
                  </div>
                  <div>
                    <span className="info-title">Fee</span>
                    <div>{humanizeCurrency(this.props.focusedContestInfo.contest.buyin)}
                    </div>
                  </div>
                </div>

                <div className="btn-enter-contest">
                  {this.getEnterContestButton()}
                </div>

              </div>
            </div>
          </div>

          <div colSpan="9" className="pane-lower">
            <ul className="tab-nav">{tabNav}</ul>
            <div className="tab-content">{this.getActiveTab()}</div>
          </div>

        </div>
      );
    }

    return (
      <div>Select a Contest</div>
    );
  },


  stripContestFromUrl() {
    this.props.routerPush('/contests/');
  },


  closePane() {
    AppActions.closePane();
  },


  enterContest(contestId) {
    this.props.enterContest(contestId, this.props.focusedLineup.id);
  },


  // Enter the currently focused lineup into a contest.
  // TODO: this is copypasta from loby-contests.jsx. THis should really be a child copmponent of
  // that but I kinda screwed up a long time ago. fix this someday.
  handleEnterContest(contest) {
    this.enterContest(contest.id);
  },


  // When a tab is clicked, tell the state to show it'scontent.
  handleTabClick(tabName) {
    this.setState({ activeTab: tabName });
  },


  render() {
    const contestDetail = this.getContest();

    return (
      <div className="cmp-contest-list__detail">
        {contestDetail}
      </div>
    );
  },

});

// Wrap the component to inject dispatch and selected state into it.
const ContestListDetailConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(ContestListDetail);

// Create an enhanced history that syncs navigation events with the store
const history = syncHistoryWithStore(browserHistory, store);

renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/contests/" component={ContestListDetailConnected} />
      <Route path="/contests/:contestId/" component={ContestListDetailConnected} />
    </Router>
  </Provider>,
  '.cmp-contest-list-detail'
);


module.exports = ContestListDetailConnected;
