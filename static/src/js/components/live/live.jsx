import LiveAnimationArea from './live-animation-area';
import LiveChooseLineup from './live-choose-lineup';
import LiveContestsPane from './live-contests-pane';
import LiveCountdown from './live-countdown';
import LiveHeader from './live-header';
import LiveLineup from './live-lineup';
import LiveLoading from './live-loading';
import LiveStandingsPane from './live-standings-pane';
import log from '../../lib/logging';
import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import { addMessage, clearMessages } from '../../actions/message-actions';
import { bindActionCreators } from 'redux';
import { checkForUpdates } from '../../actions/watching';
import { fetchCurrentEntriesAndRelated, fetchRelatedEntriesInfo } from '../../actions/entries';
import { fetchPlayerBoxScoreHistoryIfNeeded } from '../../actions/player-box-score-history-actions';
import { Provider, connect } from 'react-redux';
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
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    addMessage,
    checkForUpdates,
    clearMessages,
    fetchCurrentEntriesAndRelated,
    fetchPlayerBoxScoreHistoryIfNeeded,
    fetchRelatedEntriesInfo,
    updateLiveMode,
  }, dispatch),
});

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  draftGroupTiming: watchingDraftGroupTimingSelector(state),
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
export const Live = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    contest: React.PropTypes.object.isRequired,
    draftGroupTiming: React.PropTypes.object.isRequired,
    relevantGamesPlayers: React.PropTypes.object.isRequired,
    myLineup: React.PropTypes.object.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    params: React.PropTypes.object,
    uniqueEntries: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    return {
      setTimeoutEntries: null,
    };
  },

  /**
   * Uses promises in order to pull in all relevant data into redux, and then starts to listen for Pusher calls
   * Here's the documentation on the order in which all the data comes in https://goo.gl/uSCH0K
   */
  componentWillMount() {
    const { actions, params } = this.props;

    // update what we are watching based on where we are in the live section
    if (params.hasOwnProperty('myLineupId')) {
      actions.updateLiveMode({
        myLineupId: params.myLineupId,
        sport: params.sport,
        contestId: params.contestId || null,
        opponentLineupId: params.opponentLineupId || null,
      });

      // double check all related information is up to date
      actions.fetchPlayerBoxScoreHistoryIfNeeded(params.sport);
      actions.fetchRelatedEntriesInfo();
    }

    // force entries to refresh
    actions.fetchCurrentEntriesAndRelated(true);

    // start polling for api updates
    window.setInterval(this.props.actions.checkForUpdates, 5000);
  },

  componentWillReceiveProps(nextProps) {
    const { actions } = this.props;

    // show a message when contests are done for the night
    if (!this.props.draftGroupTiming.ended && nextProps.draftGroupTiming.ended) {
      actions.clearMessages();
      actions.addMessage({
        header: 'Contests have finished!',
        content: '<div>See your results <a href="/results/">here</a></div>',
        level: 'success',
      });
    }

    // terrible hack to poll for current-entries
    // instead, we should be looking for pusher call confirming that contests have been generated
    if (this.props.watching.myLineupId) {
      const myLineupId = this.props.watching.myLineupId;
      const myEntry = this.props.uniqueEntries.entriesObj[myLineupId] || {};
      const myNextEntry = nextProps.uniqueEntries.entriesObj[myLineupId] || {};

      if (!this.state.setTimeoutEntries && myNextEntry.contest === null && myEntry.hasStarted) {
        // check for contest_id every 5 seconds
        this.setState({ setTimeoutEntries: setInterval(() => {
          log.warn('live.currentEntriesRefresh - fetching entries');
          actions.fetchCurrentEntriesAndRelated(true);
        }, 5000) });

        // also immediately check
        actions.fetchCurrentEntriesAndRelated(true);
      }

      // stop checking once we have a contest
      if (this.state.setTimeoutEntries && myNextEntry.contest !== null) {
        log.warn('No need to try entries again');
        window.clearInterval(this.state.setTimeoutEntries);
        this.setState({ setTimeoutEntries: undefined });
      }
    }
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
    if (!uniqueEntries.haveLoaded) return (<LiveLoading isContestPools={false} />);

    // choose a lineup if we haven't yet
    if (watching.myLineupId === null && !params.hasOwnProperty('myLineupId')) {
      return (
        <div className="live__bg">
          <LiveChooseLineup
            entriesLoaded={uniqueEntries.haveLoaded}
            entries={uniqueEntries.entries}
          />
        </div>
      );
    }

    // show the countdown until it goes live
    const myEntry = uniqueEntries.entriesObj[watching.myLineupId] || {};
    if (!myEntry.hasStarted) {
      // wait to show lineup until it's loaded
      let countdownLineup;
      if (!relevantGamesPlayers.isLoading) {
        countdownLineup = (
          <LiveLineup
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
            entry={myEntry}
          />
        </div>
      );
    }

    // wait for contest_id to be returned via current-entries api
    if (myEntry.contest === null) return (<LiveLoading />);

    // wait for data to load before showing anything
    if (relevantGamesPlayers.isLoading) return (<LiveLoading isContestPools={false} />);

    // defining optional component pieces
    let liveStandingsPane;
    let opponentLineupComponent;
    let contestsPaneOpen = true;

    // if viewing a contest
    if (watching.contestId !== null && !contest.isLoading) {
      contestsPaneOpen = false;
      let standingsPaneOpen = true;

      // if viewing an opponent, add in lineup and update moneyline
      if (watching.opponentLineupId !== null && !opponentLineup.isLoading) {
        standingsPaneOpen = false;

        opponentLineupComponent = (
          <LiveLineup
            draftGroupStarted={draftGroupTiming.started}
            lineup={opponentLineup}
            watching={watching}
            whichSide="opponent"
          />
        );
      }

      liveStandingsPane = (
        <LiveStandingsPane
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
          draftGroupStarted={draftGroupTiming.started}
          lineup={myLineup}
          watching={watching}
          whichSide="mine"
        />

        {opponentLineupComponent}

        <section className="cmp-live__court-scoreboard">
          <div className="court-scoreboard__content">
            <LiveHeader
              contest={contest}
              myLineup={myLineup}
              opponentLineup={opponentLineup}
              watching={watching}
            />

            <LiveAnimationArea />
          </div>
        </section>

        <LiveContestsPane
          lineup={myLineup}
          openOnStart={contestsPaneOpen}
          watching={watching}
        />

        {liveStandingsPane}
      </div>
    );
  },
});

// Wrap the component to inject dispatch and selected state into it.
export const LiveConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Live);

// create an enhanced history that syncs navigation events with the store
const history = syncHistoryWithStore(browserHistory, store);

// url routing via react-router
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
