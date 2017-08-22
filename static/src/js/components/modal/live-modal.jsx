import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { fetchContestPoolEntries } from '../../actions/contest-pool-actions';
import AppStateStore from '../../stores/app-state-store.js';
import Modal from './modal.jsx';
import log from '../../lib/logging';
import moment from 'moment';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
const { Provider, connect } = ReactRedux;
import Cookies from 'js-cookie';

const nbaarena = require('../../../img/blocks/live-animation-stage/nba-court.png');
const nflarena = require('../../../img/blocks/live-animation-stage/nfl-field.png');
const nhlarena = require('../../../img/blocks/live-animation-stage/nhl-rink.png');
// const mlbarena = require('../../../img/blocks/live-animation-stage/mlb-field.png');

const arenamap = [
  { sport: 'nfl', asset: nflarena },
  { sport: 'nba', asset: nbaarena },
  { sport: 'nhl', asset: nhlarena },
  // { sport: 'mlb', asset: mlbarena },
];

const getArenaAsset = (sport) => {
  for (let i = 0; i < arenamap.length; i++) {
    if (arenamap[i].sport === sport) {
      return arenamap[i].asset;
    }
  }
};

const mapStateToProps = (state) => ({
  gamepools: state.contestPoolEntries,
});

const mapDispatchToProps = (dispatch) => ({
  fetchContestPoolEntries: () => dispatch(fetchContestPoolEntries()),
});

const LiveModal = React.createClass({
  propTypes: {
    onClose: React.PropTypes.func,
    showCloseButton: React.PropTypes.bool,
    gamepools: React.PropTypes.object,
    fetchContestPoolEntries: React.PropTypes.func,
  },

  defaultProps: {
    showCloseButton: true,
  },

  componentWillMount() {
    // TODO: will need to check cookie id with current event
    this.props.fetchContestPoolEntries();
    this.interval = setInterval(() => {this.tick();}, 1500);
    this.setState({
      isOpen: true,
    });
  },

  componentWillUnmount() {
    clearInterval(this.interval);
  },

  onClose() {
    this.setState({
      isOpen: false,
    });
    AppStateStore.modalClosed();
  },

  getUpcomingGame(entrypools) {
    for (const entryid in entrypools.entries) {
      if (entrypools.entries.hasOwnProperty(entryid)) {
        const sportasset = getArenaAsset(entrypools.entries[entryid].sport);
        const start = moment(entrypools.entries[entryid].start, moment.ISO_8601).format('h:mma');
        const entry = entrypools.entries[entryid];

        return { sportasset, entry, start };
      }
    }
  },

  tick() {
    const pools = this.getUpcomingGame(this.props.gamepools);
    for (const entry in pools) {
      if (pools.hasOwnProperty(entry) && entry === 'entry') {
        log.info(pools[entry].id);
        const entryId = pools[entry].id;
        if (this.hasBeenDismissed(entryId) && this.isUpcoming()) {
          this.iopenModel();
        }
      }
    }
  },

  hasBeenDismissed(entryId) {
    return Cookies.get(entryId) === 'true';
  },

  isUpcoming(date) {

  },

  iopenModel() {
    this.setState({
      isOpen: true,
    });
    AppStateStore.modalOpened();
  },

  render() {
    return (
      <Modal
        showCloseBtn={this.props.showCloseButton}
        isOpen={this.state.isOpen}
        onClose={this.onClose}
        className="live-notice"
      >
        <div>
          <header className="cmp-modal__header">IT’S GAME TIME!</header>
          <div className="content">
            <p>Your  contest(s) is(are) starting! Follow all the
action in our live section or head back to the
lobby and draft a team for tomorrow's contests.</p>
          </div>
        </div>
      </Modal>
    );
  },
});

export const LiveConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveModal);

const history = syncHistoryWithStore(browserHistory, store);

renderComponent(
  <Provider store={ store }>
    <Router history={ history }>
      <Route path="/live/*" component={ LiveConnected } />
      <Route path="/contests/*" component={ LiveConnected } />
      <Route path="/results/*" component={ LiveConnected } />
      <Route path="/account/*" component={ LiveConnected } />
    </Router>
  </Provider>,
  '.cmp-live-message-display'
);


module.exports = LiveModal;
