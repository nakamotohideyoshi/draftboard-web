import * as ReactRedux from 'react-redux';
import React from 'react';
import renderComponent from '../../lib/render-component';
import { filter as _filter } from 'lodash';
import { push as routerPush } from 'react-router-redux';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';

import LiveAnimationArea from './live-animation-area';
import LiveBottomNav from './live-bottom-nav';
import LiveContestsPane from './live-contests-pane';
import LiveCountdown from './live-countdown';
import LiveHeader from './live-header';
import LiveLineup from './live-lineup';
import LiveLineupSelectModal from './live-lineup-select-modal';
import LiveMoneyline from './live-moneyline';
import LiveStandingsPaneConnected from './live-standings-pane';
import log from '../../lib/logging';
import store from '../../store';
import { addMessage, clearMessages } from '../../actions/message-actions';
import { checkForUpdates } from '../../actions/live';
import { currentLineupsSelector } from '../../selectors/current-lineups';
import { fetchContestLineups } from '../../actions/live-contests';
import { fetchContestLineupsUsernamesIfNeeded } from '../../actions/live-contests';
import { fetchEntriesIfNeeded } from '../../actions/entries';
import { fetchPlayerBoxScoreHistoryIfNeeded } from '../../actions/player-box-score-history-actions';
import { fetchRelatedEntriesInfo } from '../../actions/entries';
import { fetchUpcomingLineups } from '../../actions/entries';
import { liveContestsSelector } from '../../selectors/live-contests';
import { liveSelector } from '../../selectors/live';
import { sportsSelector } from '../../selectors/sports';
import { updateLiveMode } from '../../actions/live';


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
});

/*
 * The overarching component for the live section.
 */
const Live = React.createClass({

  propTypes: {
    currentLineupsSelector: React.PropTypes.object.isRequired,
    dispatch: React.PropTypes.func.isRequired,
    liveContestsSelector: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    params: React.PropTypes.object,
    sportsSelector: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    return {
      isLoaded: false,
      calledUpcomingLineups: false,
    };
  },

  /**
   * Uses promises in order to pull in all relevant data into redux, and then starts to listen for Pusher calls
   * Here's the documentation on the order in which all the data comes in https://goo.gl/uSCH0K
   */
  componentWillMount() {
    // update mode based on where we are in the live section
    const urlParams = this.props.params;
    if (urlParams.hasOwnProperty('myLineupId')) {
      this.props.dispatch(updateLiveMode({
        myLineupId: urlParams.myLineupId,
        sport: urlParams.sport,
        contestId: urlParams.contestId || undefined,
        opponentLineupId: urlParams.opponentLineupId || undefined,
      }));

      // double check all related information is up to date
      this.props.dispatch(fetchRelatedEntriesInfo());
      this.props.dispatch(fetchPlayerBoxScoreHistoryIfNeeded(urlParams.sport));
    } else {
      // force entries to refresh
      this.props.dispatch(fetchEntriesIfNeeded(true));
    }

    // start listening for pusher calls, and server updates
    this.startParityChecks();

    setTimeout(() => this.setState({ isLoaded: true }), 500);
  },

  componentWillReceiveProps(nextProps) {
    if (this.props.liveSelector.draftGroupEnded === false && nextProps.liveSelector.draftGroupEnded === true) {
      store.dispatch(clearMessages());
      store.dispatch(addMessage({
        header: 'Contests have finished!',
        content: '<div>See your results <a href="/results/">here</a></div>',
        level: 'success',
      }));
    }
  },

  componentDidUpdate(prevProps) {
    const liveData = this.props.liveSelector;

    // when we get related info
    if (liveData.draftGroupStarted === false &&
        prevProps.liveSelector.draftGroupStarted === true
    ) {
      this.props.dispatch(fetchUpcomingLineups());
    }
  },

  /*
   * Since we base the live section on the redux store.live substore, we have to have this method to update both the
   * redux substore AND the url push state, so a user can go "back"
   * @param  {string} path The URL path to push
   * @param  {object} changedFields The changed fields in store.live substore
   */
  changePathAndMode(path, changedFields) {
    log.debug('Live.changePathAndMode()', path);

    // update the URL path
    this.props.dispatch(routerPush(path));

    // update redux store mode
    this.props.dispatch(updateLiveMode(changedFields));

    // if the contest has changed, then get the appropriate usernames for the standings pane
    if (changedFields.hasOwnProperty('contestId')) {
      this.props.dispatch(fetchContestLineupsUsernamesIfNeeded(changedFields.contestId));
    }
  },

  /**
   * Force a refresh fo draft groups. Called by the countdown when time is up
   */
  forceContestLineupsRefresh() {
    log.info('Live.forceContestLineupsRefresh()');
    const contestEntry = _filter(this.props.liveSelector.entries,
      (entry) => entry.lineup === this.props.liveSelector.mode.myLineupId
    )[0];

    this.props.dispatch(
      fetchContestLineups(contestEntry.contest, contestEntry.sport)
    ).then(() =>
      this.props.dispatch(fetchRelatedEntriesInfo())
    );
  },

  /**
   * Periodically override the redux state with server data, to ensure that we have up to date data in case we missed
   * a Pusher call here or there. In time the intervals will increase, as we gain confidence in the system.
   */
  startParityChecks() {
    const parityChecks = {
      liveUpdate: window.setInterval(() => this.props.dispatch(checkForUpdates()), 5000),
    };

    // add the checsk to the state in case we need to clearInterval in the future
    this.setState({ boxScoresIntervalFunc: parityChecks });
  },

  /*
   * This loading screen shows in lieu of the live section when it takes longer than a second to do an initial load
   * TODO Live - get built out
   *
   * @return {JSXElement}
   */
  renderLoadingScreen() {
    return (
      <div className="live__bg">
        <div className="live--loading">
          <div className="preload-court" />
          <div className="spinner">
            <div className="double-bounce1" />
            <div className="double-bounce2" />
          </div>
        </div>
      </div>
    );
  },

  render() {
    const liveData = this.props.liveSelector;
    const mode = liveData.mode;

    // defining optional component pieces
    let liveStandingsPane;
    let moneyLine;
    let opponentLineupComponent;

    // if a lineup has not been chosen yet
    if (mode.hasOwnProperty('myLineupId') === false &&
        liveData.hasOwnProperty('entries')
    ) {
      return (
        <div className="live__bg">
          <LiveLineupSelectModal
            changePathAndMode={this.changePathAndMode}
            entriesLoaded={liveData.entriesHaveLoaded}
            entries={liveData.entries}
          />
        </div>
      );
    }

    // wait for data to load before showing anything
    if (liveData.hasRelatedInfo === false || this.state.isLoaded === false) {
      return this.renderLoadingScreen();
    }

    const myLineup = liveData.lineups.mine || {};

    // show the countdown until it goes live
    if (liveData.draftGroupStarted === false) {
      return (
        <div className={`live__bg live--countdown live--sport-${myLineup.draftGroup.sport}`}>
          <LiveLineup
            changePathAndMode={this.changePathAndMode}
            draftGroupStarted={false}
            games={this.props.sportsSelector.games}
            lineup={myLineup}
            mode={mode}
            sport={myLineup.draftGroup.sport}
            whichSide="mine"
          />
          <LiveCountdown
            onCountdownComplete={this.forceContestLineupsRefresh}
            lineup={myLineup}
          />
        </div>
      );
    }

    // wait until the lineup data has loaded before rendering
    if (liveData.lineups.hasOwnProperty('mine') && myLineup.roster !== undefined) {
      // if viewing a contest, then add standings pane and moneyline
      if (mode.contestId) {
        const contest = liveData.contest;
        let opponentWinPercent;

        liveStandingsPane = (
          <LiveStandingsPaneConnected
            changePathAndMode={this.changePathAndMode}
            contest={contest}
            lineups={contest.lineups}
            rankedLineups={contest.rankedLineups}
            mode={mode}
          />
        );

        // if viewing an opponent, add in lineup and update moneyline
        if (mode.opponentLineupId) {
          const opponentLineup = liveData.lineups.opponent;

          // if not villian watch, then show opponent
          if (opponentLineup.id !== 1) {
            opponentWinPercent = opponentLineup.opponentWinPercent;
          }

          opponentLineupComponent = (
            <LiveLineup
              changePathAndMode={this.changePathAndMode}
              draftGroupStarted={liveData.draftGroupStarted}
              games={this.props.sportsSelector.games}
              lineup={opponentLineup}
              mode={mode}
              sport={myLineup.draftGroup.sport}
              whichSide="opponent"
            />
          );
        }

        moneyLine = (
          <section className="live-moneyline live-moneyline--contest-overall">
            <LiveMoneyline
              percentageCanWin={contest.percentageCanWin}
              myWinPercent={myLineup.myWinPercent}
              opponentWinPercent={opponentWinPercent}
            />
          </section>
        );
      }

      return (
        <div className={`live__bg live--sport-${myLineup.draftGroup.sport}`}>
          <LiveLineup
            changePathAndMode={this.changePathAndMode}
            draftGroupStarted={liveData.draftGroupStarted}
            games={this.props.sportsSelector.games}
            lineup={myLineup}
            mode={mode}
            sport={myLineup.draftGroup.sport}
            whichSide="mine"
          />

          {opponentLineupComponent}

          <section className="cmp-live__court-scoreboard">
            <div className="court-scoreboard__content">
              <LiveHeader
                changePathAndMode={this.changePathAndMode}
                liveSelector={liveData}
              />

              <LiveAnimationArea
                liveSelector={liveData}
                sport={mode.sport}
              />

              {moneyLine}

              <LiveBottomNav
                hasContest={mode.contestId !== undefined}
              />
            </div>
          </section>

          <LiveContestsPane
            changePathAndMode={this.changePathAndMode}
            lineup={myLineup}
            mode={mode}
          />

          {liveStandingsPane}
        </div>
      );
    }

    // TODO Live - make a loading screen if it takes longer than a second to load
    return this.renderLoadingScreen();
  },
});

// Set up Redux connections to React
const { Provider, connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
const LiveConnected = connect(
  mapStateToProps
)(Live);

// Create an enhanced history that syncs navigation events with the store
const history = syncHistoryWithStore(browserHistory, store);

// Uses the Provider and Routes in order to have URL routing via redux-simple-router and redux state
renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/live/" component={LiveConnected} />
      <Route path="/live/:sport/lineups/:myLineupId" component={LiveConnected} />
      <Route path="/live/:sport/lineups/:myLineupId/contests/:contestId/" component={LiveConnected} />
      <Route
        path="/live/:sport/lineups/:myLineupId/contests/:contestId/opponents/:opponentLineupId"
        component={LiveConnected}
      />
    </Router>
  </Provider>,
  '.cmp-live'
);
