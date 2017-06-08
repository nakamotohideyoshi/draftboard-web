import merge from 'lodash/merge';
import { Provider, connect } from 'react-redux';
import React from 'react';
import LiveAnimationArea from '../live/live-animation-area';
import LiveHeader from '../live/live-header';
import LiveBigPlays from '../live/live-big-plays';
import LiveStandingsPane from '../live/live-standings-pane';
import DebugMenu from './debug-menu';
import store from '../../store';
import fpoState from './fixtures/state';
import { addEventAndStartQueue } from '../../actions/events';
import { Router, Route, browserHistory } from 'react-router';
import renderComponent from '../../lib/render-component';
import { syncHistoryWithStore } from 'react-router-redux';
import { push as routerPush } from 'react-router-redux';

require('../../../sass/blocks/live-debugger.scss');

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  currentEvent: state.events.currentEvent,
  bigEvents: state.events.bigEvents,
});

export const DebugLiveAnimationsPage = connect(mapStateToProps)(React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
    bigEvents: React.PropTypes.array,
    params: React.PropTypes.object,
  },

  getInitialState() {
    return {
      sport: this.props.params.sport || 'nba',
      play: this.props.params.play || null,
    };
  },

  componentWillMount() {
    window.is_debugging_live_animation = true;
  },

  componentDidMount() {
    if (this.props.params.play !== null) {
      window.pbpQueue.gotoPBPById(this.props.params.play);
    }
  },

  onSportUpdated(sport) {
    if (this.state.sport !== sport) {
      store.dispatch(routerPush(`/debug/live-animations/${sport}/`));
      this.setState({ sport });
    }
  },

  onPBPUpdated(message) {
    if (!message) {
      return;
    }

    const eventType = 'pbp';
    const sport = message.sport;
    const gameId = message.gameId;
    const messageId = message.id;
    const gameEvent = merge(message, { id: new Date().getTime() });

    store.dispatch(routerPush(`/debug/live-animations/${sport}/plays/${messageId}/`));
    store.dispatch(addEventAndStartQueue(gameId, gameEvent, eventType, sport));
  },

  render() {
    const { eventsMultipart, watching, contest } = fpoState;
    const { currentEvent, bigEvents } = this.props;

    watching.sport = this.state.sport;

    return (
      <div className="live">
        <DebugMenu
          sport={this.state.sport}
          play={this.state.play}
          onSportUpdated={(sport) => this.onSportUpdated(sport)}
          onPBPUpdated={(pbp) => this.onPBPUpdated(pbp)}
        />
        <section className="live__venues">
          <LiveHeader
            {...{ contest, currentEvent, watching }}
            lineups={fpoState.uniqueLineups.lineups}
            myLineup={fpoState.myLineupInfo}
            opponentLineup={fpoState.opponentLineup}
            selectLineup={fpoState.selectLineup}
          />
          <LiveAnimationArea {...{ currentEvent, eventsMultipart, watching }} />
          <LiveStandingsPane {...{ contest, watching }} />
        </section>
        <LiveBigPlays queue={bigEvents || []} />
      </div>
    );
  },
}));

// create an enhanced history that syncs navigation events with the store
const history = syncHistoryWithStore(browserHistory, store);

// url routing via react-router
renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="debug/live-animations(/:sport)" component={DebugLiveAnimationsPage} />
      <Route path="debug/live-animations/:sport/plays/:play" component={DebugLiveAnimationsPage} />
    </Router>
  </Provider>,
  '#cmp-live-debugger'
);
