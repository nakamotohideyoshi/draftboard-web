import DebugLiveAnimationsPage from '../live-debugger/live-debugger';
import LiveAnimationArea from './live-animation-area';
import LiveChooseLineup from './live-choose-lineup';
import LiveBigPlays from './live-big-plays';
import LiveContestsPane from './live-contests-pane';
import LiveCountdown from './live-countdown';
import LiveHeader from './live-header';
import LiveLineup from './live-lineup';
import LiveLoading from './live-loading';
import LiveStandingsPane from './live-standings-pane';
import LiveUnsupported from './live-unsupported';
import log from '../../lib/logging';
import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import { addMessage, clearMessages } from '../../actions/message-actions';
import { bigPlaysSelector } from '../../selectors/live-big-plays';
import { bindActionCreators } from 'redux';
import { checkForUpdates } from '../../actions/watching';
import { fetchCurrentLineupsAndRelated, fetchRelatedLineupsInfo } from '../../actions/current-lineups';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';
import { Provider, connect } from 'react-redux';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { uniqueLineupsSelector } from '../../selectors/current-lineups';
import { updateLiveMode, updateWatchingAndPath } from '../../actions/watching';
import {
  watchingContestSelector,
  watchingDraftGroupTimingSelector,
  watchingMyLineupSelector,
  relevantGamesPlayersSelector,
  watchingOpponentLineupSelector,
} from '../../selectors/watching';


// get custom logger for actions
const logComponent = log.getLogger('component');

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
    fetchCurrentLineupsAndRelated,
    fetchRelatedLineupsInfo,
    updateLiveMode,
    updateWatchingAndPath,
  }, dispatch),
});

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  bigPlaysQueue: bigPlaysSelector(state),
  draftGroupTiming: watchingDraftGroupTimingSelector(state),
  relevantGamesPlayers: relevantGamesPlayersSelector(state),
  contest: watchingContestSelector(state),
  myLineupInfo: watchingMyLineupSelector(state),
  opponentLineup: watchingOpponentLineupSelector(state),
  uniqueLineups: uniqueLineupsSelector(state),
  watching: state.watching,
  currentEvent: state.events.currentEvent,
  eventsMultipart: state.eventsMultipart,
});

/*
 * The overarching component for the live section.
 */
export const Live = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    bigPlaysQueue: React.PropTypes.array.isRequired,
    contest: React.PropTypes.object.isRequired,
    draftGroupTiming: React.PropTypes.object.isRequired,
    relevantGamesPlayers: React.PropTypes.object.isRequired,
    myLineupInfo: React.PropTypes.object.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    params: React.PropTypes.object,
    uniqueLineups: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    currentEvent: React.PropTypes.object,
    eventsMultipart: React.PropTypes.object,
  },

  getInitialState() {
    return {
      setTimeoutEntries: null,
      windowWidth: window.innerWidth,
    };
  },

  /**
   * Uses promises in order to pull in all relevant data into redux, and then starts to listen for Pusher calls
   * Here's the documentation on the order in which all the data comes in https://goo.gl/uSCH0K
   */
  componentWillMount() {
    const { actions, params } = this.props;

    // to show message if unsupported size
    window.addEventListener('resize', this.handleResize);

    // update what we are watching based on where we are in the live section
    if (params.hasOwnProperty('myLineupId')) {
      actions.updateLiveMode({
        myLineupId: params.myLineupId,
        sport: params.sport,
        contestId: params.contestId || null,
        opponentLineupId: params.opponentLineupId || null,
      });
    }

    // force lineups to refresh, then checks everything else is up to date
    actions.fetchCurrentLineupsAndRelated(true);

    // start polling for api updates
    window.setInterval(this.props.actions.checkForUpdates, 5000);
  },

  componentWillReceiveProps(nextProps) {
    const { actions, watching } = this.props;

    // show a message when contests are done for the night
    if (!this.props.draftGroupTiming.ended && nextProps.draftGroupTiming.ended) {
      actions.clearMessages();
      actions.addMessage({
        header: 'Contests have finished!',
        content: '<div>See your results <a href="/results/">here</a></div>',
        level: 'success',
      });
    }

    // terrible hack to poll for current-lineups
    // instead, we should be looking for pusher call confirming that contests have been generated
    if (watching.myLineupId) {
      const myLineupId = watching.myLineupId;
      const myLineup = this.props.uniqueLineups.lineupsObj[myLineupId] || {};
      const myLineupNext = nextProps.uniqueLineups.lineupsObj[myLineupId] || {};
      const myContestNext = myLineupNext.contests || [];

      // when the countdown ends, we trigger a fetchCurrentLineupsAndRelated call
      // which then jumpstarts this if there are no contests yet
      if (!this.state.setTimeoutEntries && myLineup.hasStarted && myContestNext.length === 0) {
        // check for contest_id every 5 seconds
        this.setState({ setTimeoutEntries: setInterval(() => {
          logComponent.warn('live.currentEntriesRefresh - fetching lineups');
          actions.fetchCurrentLineupsAndRelated(true);
        }, 5000) });

        // also immediately check
        // actions.fetchCurrentLineupsAndRelated(true);
      }

      // if there's only one contest, default to it
      if (
        watching.contestId === null &&
        myLineup.hasStarted &&
        myLineupNext.contests &&
        myLineupNext.contests.length === 1
      ) {
        const contestId = myLineupNext.contests[0];
        const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/contests/${contestId}/`;
        const changedFields = {
          contestId,
        };

        actions.updateWatchingAndPath(path, changedFields);
      }

      // stop checking once we have a contest
      if (this.state.setTimeoutEntries && myContestNext.length > 0) {
        log.warn('No need to try lineups again');
        window.clearInterval(this.state.setTimeoutEntries);
        this.setState({ setTimeoutEntries: null });
      }
    }
  },

  // remove event handler
  componentWillUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },

  handleResize() {
    this.setState({ windowWidth: window.innerWidth });
  },

  selectLineup(lineup) {
    const { actions } = this.props;
    const path = `/live/${lineup.sport}/lineups/${lineup.id}/`;
    const changedFields = {
      draftGroupId: lineup.draftGroup,
      myLineupId: lineup.id,
      sport: lineup.sport,
    };

    actions.updateWatchingAndPath(path, changedFields);
    actions.fetchCurrentLineupsAndRelated(true);
  },

  render() {
    const {
      actions,
      bigPlaysQueue,
      contest,
      draftGroupTiming,
      myLineupInfo,
      opponentLineup,
      params,
      relevantGamesPlayers,
      uniqueLineups,
      watching,
    } = this.props;

    // BEM CSS block name
    const block = 'live';

    if (this.state.windowWidth < 768) return (<LiveUnsupported />);

    // don't do anything until we have lineups!
    if (!uniqueLineups.haveLoaded) return (<div className={`${block}`}><LiveLoading isContestPools={false} /></div>);

    // choose a lineup if we haven't yet
    if (watching.myLineupId === null && !params.hasOwnProperty('myLineupId')) {
      return (
        <div className={`${block}`}>
          <LiveChooseLineup
            selectLineup={this.selectLineup}
            lineupsLoaded={uniqueLineups.haveLoaded}
            lineups={uniqueLineups.lineups}
          />
        </div>
      );
    }

    // show the countdown until it goes live
    const myLineup = uniqueLineups.lineupsObj[watching.myLineupId] || {};
    if (!myLineup.hasStarted) {
      // wait to show lineup until it's loaded
      let countdownLineup;
      if (!relevantGamesPlayers.isLoading) {
        countdownLineup = (
          <LiveLineup
            draftGroupStarted={false}
            lineup={myLineupInfo}
            watching={watching}
            whichSide="mine"
          />
        );
      }

      // but immediately show the countdown
      const classNames = generateBlockNameWithModifiers(block, ['countdown', `sport-${watching.sport}`]);
      return (
        <div className={classNames}>
          {countdownLineup}
          <LiveCountdown
            onCountdownOver={() => actions.fetchCurrentLineupsAndRelated(true)}
            lineup={myLineup}
          />
        </div>
      );
    }

    // wait for contest_id to be returned via current-lineups api
    if (myLineup.contests.length === 0) {
      return (<div className={`${block}`}><LiveLoading isContestPools /></div>);
    }

    // wait for data to load before showing anything
    if (relevantGamesPlayers.isLoading) {
      return (<div className={`${block}`}><LiveLoading isContestPools={false} /></div>);
    }

    // defining optional component pieces
    let liveBigPlaysDom;
    let liveStandingsPane;
    let opponentLineupComponent;
    let contestsPaneOpen = true;
    let venuesPosition = '';
    const modifiers = [`sport-${watching.sport}`];

    // if viewing a contest
    if (watching.contestId !== null && !contest.isLoading) {
      contestsPaneOpen = false;

      // if viewing an opponent, add in lineup and update moneyline
      if (watching.opponentLineupId !== null && !opponentLineup.isLoading) {
        venuesPosition = 'showing-opponent-lineup';

        opponentLineupComponent = (
          <LiveLineup
            contest={contest}
            draftGroupStarted={draftGroupTiming.started}
            lineup={opponentLineup}
            watching={watching}
            whichSide="opponent"
          />
        );
      }

      liveStandingsPane = <LiveStandingsPane contest={contest} watching={watching} />;
    }

    modifiers.push(venuesPosition);
    const classNames = generateBlockNameWithModifiers(block, modifiers);

    if (bigPlaysQueue.length > 0) liveBigPlaysDom = (<LiveBigPlays queue={bigPlaysQueue} />);

    return (
      <div className={classNames}>
        <LiveLineup
          contest={contest}
          draftGroupStarted={draftGroupTiming.started}
          lineup={myLineupInfo}
          watching={watching}
          whichSide="mine"
        />

        {opponentLineupComponent}

        <section className={`${block}__venues`}>
          <LiveHeader
            contest={contest}
            lineups={uniqueLineups.lineups}
            myLineup={myLineupInfo}
            opponentLineup={opponentLineup}
            selectLineup={this.selectLineup}
            watching={watching}
            currentEvent={this.props.currentEvent}
            eventsMultipart={this.props.eventsMultipart}
          />

          <LiveAnimationArea
            watching={ this.props.watching }
            currentEvent={ this.props.currentEvent }
            eventsMultipart={ this.props.eventsMultipart }
          />
          {liveStandingsPane}
        </section>

        <LiveContestsPane
          lineup={myLineupInfo}
          openOnStart={contestsPaneOpen}
          watching={watching}
        />

        {liveBigPlaysDom}
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
      <Route path="debug/live-animations" component={DebugLiveAnimationsPage} />
    </Router>
  </Provider>,
  '#cmp-live'
);
