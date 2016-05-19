import * as ReactRedux from 'react-redux';
import filter from 'lodash/filter';
import LiveAnimationArea from './live-animation-area';
import LiveContestsPane from './live-contests-pane';
import LiveCountdown from './live-countdown';
import LiveHeader from './live-header';
import LiveLineup from './live-lineup';
import LiveLineupSelectModal from './live-lineup-select-modal';
import LiveStandingsPane from './live-standings-pane';
import log from '../../lib/logging';
import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import { addMessage, clearMessages } from '../../actions/message-actions';
import { checkForUpdates } from '../../actions/watching';
import { fetchContestLineups } from '../../actions/live-contests';
import { fetchContestLineupsUsernamesIfNeeded } from '../../actions/live-contests';
import { fetchEntriesIfNeeded } from '../../actions/entries';
import { fetchPlayerBoxScoreHistoryIfNeeded } from '../../actions/player-box-score-history-actions';
import { fetchRelatedEntriesInfo } from '../../actions/entries';
import { fetchUpcomingLineups } from '../../actions/entries';
import { push as routerPush } from 'react-router-redux';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { uniqueEntriesSelector } from '../../selectors/entries';
import { updateLiveMode } from '../../actions/watching';
import {
  watchingContestSelector,
  watchingDraftGroupTimingSelector,
  watchingMyLineupSelector,
  relevantGamesPlayersSelector,
  watchingOpponentLineupSelector,
} from '../../selectors/watching';

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  draftGroupTiming: watchingDraftGroupTimingSelector(state),
  eventsMultipart: state.eventsMultipart,
  relevantGamesPlayers: relevantGamesPlayersSelector(state),
  contest: watchingContestSelector(state),
  myLineup: watchingMyLineupSelector(state),
  opponentLineup: watchingOpponentLineupSelector(state),
  uniqueEntries: uniqueEntriesSelector(state),
  watching: state.watching,
});

/*
 * The overarching component for the live section.
 */
const Live = React.createClass({

  propTypes: {
    contest: React.PropTypes.object.isRequired,
    dispatch: React.PropTypes.func.isRequired,
    draftGroupTiming: React.PropTypes.object.isRequired,
    eventsMultipart: React.PropTypes.object.isRequired,
    relevantGamesPlayers: React.PropTypes.object.isRequired,
    myLineup: React.PropTypes.object.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    params: React.PropTypes.object,
    uniqueEntries: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  /**
   * Uses promises in order to pull in all relevant data into redux, and then starts to listen for Pusher calls
   * Here's the documentation on the order in which all the data comes in https://goo.gl/uSCH0K
   */
  componentWillMount() {
    // update what we are watching based on where we are in the live section
    const urlParams = this.props.params;
    if (urlParams.hasOwnProperty('myLineupId')) {
      this.props.dispatch(updateLiveMode({
        myLineupId: urlParams.myLineupId,
        sport: urlParams.sport,
        contestId: urlParams.contestId || null,
        opponentLineupId: urlParams.opponentLineupId || null,
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
  },

  componentWillReceiveProps(nextProps) {
    if (this.props.draftGroupTiming.ended === false && nextProps.draftGroupTiming.ended === true) {
      store.dispatch(clearMessages());
      store.dispatch(addMessage({
        header: 'Contests have finished!',
        content: '<div>See your results <a href="/results/">here</a></div>',
        level: 'success',
      }));
    }
  },

  componentDidUpdate(prevProps) {
    const draftGroupTiming = this.props.draftGroupTiming;

    // when we get related info
    if (draftGroupTiming.started === false &&
        prevProps.draftGroupTiming.started === true
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
    log.debug('Live.changePathAndMode()', path, changedFields);

    // update the URL path
    this.props.dispatch(routerPush(path));

    // update what user is watching
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
    const contestEntry = filter(this.props.uniqueEntries.entries,
      (entry) => entry.lineup === this.props.watching.myLineupId
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
    const {
      contest,
      draftGroupTiming,
      myLineup,
      opponentLineup,
      params,
      relevantGamesPlayers,
      uniqueEntries,
      watching,
    } = this.props;

    // don't do anything until we have entries!
    if (uniqueEntries.haveLoaded === false) return this.renderLoadingScreen();

    // choose a lineup if we haven't yet
    if (watching.myLineupId === null && params.hasOwnProperty('myLineupId') === false) {
      return (
        <div className="live__bg">
          <LiveLineupSelectModal
            changePathAndMode={this.changePathAndMode}
            entriesLoaded={uniqueEntries.haveLoaded}
            entries={uniqueEntries.entries}
          />
        </div>
      );
    }

    // show the countdown until it goes live
    const myEntry = uniqueEntries.entriesObj[watching.myLineupId] || {};
    if (!myEntry.hasStarted) {
      // wait to show lineup until it's ready
      let countdownLineup;
      if (relevantGamesPlayers.isLoading === false) {
        countdownLineup = (
          <LiveLineup
            changePathAndMode={this.changePathAndMode}
            draftGroupStarted={false}
            lineup={myLineup}
            watching={watching}
            whichSide="mine"
          />
        );
      }

      // but immediately show the countdown
      return (
        <div className={`live__bg live--countdown live--sport-${watching.sport}`}>
          {countdownLineup}
          <LiveCountdown
            onCountdownComplete={this.forceContestLineupsRefresh}
            entry={myEntry}
          />
        </div>
      );
    }

    // wait for data to load before showing anything
    if (relevantGamesPlayers.isLoading) return this.renderLoadingScreen();

    // defining optional component pieces
    let liveStandingsPane;
    let opponentLineupComponent;
    let contestsPaneOpen = true;

    // if viewing a contest, then add standings pane and moneyline
    if (watching.contestId !== null && !contest.isLoading) {
      contestsPaneOpen = false;
      let standingsPaneOpen = true;

      // if viewing an opponent, add in lineup and update moneyline
      if (watching.opponentLineupId !== null && !opponentLineup.isLoading) {
        standingsPaneOpen = false;

        opponentLineupComponent = (
          <LiveLineup
            changePathAndMode={this.changePathAndMode}
            draftGroupStarted={draftGroupTiming.started}
            lineup={opponentLineup}
            watching={watching}
            whichSide="opponent"
          />
        );
      }

      liveStandingsPane = (
        <LiveStandingsPane
          changePathAndMode={this.changePathAndMode}
          contest={contest}
          lineups={contest.lineups}
          openOnStart={standingsPaneOpen}
          rankedLineups={contest.rankedLineups}
          watching={watching}
        />
      );
    }

    return (
      <div className={`live__bg live--sport-${watching.sport}`}>
        <LiveLineup
          changePathAndMode={this.changePathAndMode}
          draftGroupStarted={draftGroupTiming.started}
          lineup={myLineup}
          watching={watching}
          whichSide="mine"
        />

        {opponentLineupComponent}

        <section className="cmp-live__court-scoreboard">
          <div className="court-scoreboard__content">
            <LiveHeader
              changePathAndMode={this.changePathAndMode}
              contest={contest}
              myLineup={myLineup}
              opponentLineup={opponentLineup}
              watching={watching}
            />

            <LiveAnimationArea
              eventsMultipart={this.props.eventsMultipart}
              sport={watching.sport}
              watching={watching}
            />
          </div>
        </section>

        <LiveContestsPane
          changePathAndMode={this.changePathAndMode}
          lineup={myLineup}
          openOnStart={contestsPaneOpen}
          watching={watching}
        />

        {liveStandingsPane}
      </div>
    );
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
