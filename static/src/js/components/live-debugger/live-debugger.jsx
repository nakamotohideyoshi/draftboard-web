import { Provider, connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import React from 'react';
import LiveVenue from '../live/live-venue';
import DebugMenu from './debug-menu';
import store from '../../store';
import fpoState from './fixtures/state';
import { onPBPReceived } from '../../actions/events/pbp';
import { Router, Route, browserHistory } from 'react-router';
import renderComponent from '../../lib/render-component';
import { syncHistoryWithStore } from 'react-router-redux';
import { push as routerPush } from 'react-router-redux';
import { clearCurrentAnimationEvent } from '../../actions/events';

require('../../../sass/blocks/live-debugger.scss');

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  currentEvent: state.events.currentEvent,
});

const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    clearCurrentAnimationEvent,
  }, dispatch),
});

export const DebugLiveAnimationsPage = connect(mapStateToProps, mapDispatchToProps)(React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    currentEvent: React.PropTypes.object,
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
    window.DEBUG_LIVE_ANIMATIONS_CLIPS = true;
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
    const sport = message.sport;
    const id = message.id;

    store.dispatch(routerPush(`/debug/live-animations/${sport}/plays/${id}/`));
    store.dispatch(onPBPReceived(message, sport));
  },

  animationCompleted() {
    this.props.actions.clearCurrentAnimationEvent();
  },

  render() {
    const { currentEvent } = this.props;

    const {
      eventsMultipart,
      watching,
      contest,
      uniqueLineups,
      opponentLineup,
      myLineupInfo,
    } = fpoState;

    watching.sport = this.state.sport;

    return (
      <div className={ `live live--sport live--sport-${this.state.sport}`}>
        <DebugMenu
          sport={this.state.sport}
          play={this.state.play}
          onSportUpdated={(sport) => this.onSportUpdated(sport)}
          onPBPUpdated={(pbp) => this.onPBPUpdated(pbp)}
        />
        <LiveVenue
          {...{
            contest,
            currentEvent,
            watching,
            opponentLineup,
            myLineupInfo,
            eventsMultipart,
            uniqueLineups,
          } }
          onAnimationCompleted={() => this.animationCompleted()}
        />
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
