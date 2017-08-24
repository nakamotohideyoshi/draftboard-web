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
      sportasset: '',
      isOpen: false,
      sport: '',
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

  tick() {
    const pools = this.props.gamepools.entries;
    for (const entry in pools) {
      if (pools.hasOwnProperty(entry)) {
        const entryId = pools[entry].id.toString();
        const sport = pools[entry].sport;
        const start = pools[entry].start;
        if (this.hasntBeenDismissed(entryId) && this.isUpcoming(start)) {
          this.openModel(sport);
          // we can set this immediately
          // this accidentally handles events that come up at the same time ;)
          log.info(entryId);

          Cookies.set(entryId, 'true');
          log.info(Cookies.get(entryId));
        }
      }
    }
  },

  hasntBeenDismissed(entryId) {
    return Cookies.get(entryId.toString()) !== 'true';
  },

  isUpcoming(timestamp) {
    const eventTime = moment.utc(timestamp);
    const currentTime = moment(new Date().getTime()).utc();
    const diffTime = eventTime - currentTime;
    const minutes = Math.floor(moment.duration(diffTime).asMinutes());

    return minutes <= 5;
  },

  openModel(sport) {
    this.setState({
      sportasset: getArenaAsset(sport),
      isOpen: true,
      sport,
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
          <div className="content">

            <img src={ this.state.sportasset } alt="" className="arena-live-modal" />
            <h3 className="cmp-modal__header">IT’S GAME TIME!</h3>
            <p>Your <span className="sport">{ this.state.sport }</span> contest(s) is(are) starting! Follow all the
action in our live section or head back to the
lobby and draft a team for tomorrow's contests.</p>
            <a href="/live" className="button button--gradient button--med">WATCH LIVE</a>
            <a href="/" className="escape_hatch">Back to Lobby</a>
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
      <Route path="/contests/*" component={ LiveConnected } />
      <Route path="/results/*" component={ LiveConnected } />
      <Route path="/account/*" component={ LiveConnected } />
    </Router>
  </Provider>,
  '.cmp-live-message-display'
);


module.exports = LiveModal;
