import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { fetchContestPoolEntries } from '../../actions/contest-pool-actions';
import AppStateStore from '../../stores/app-state-store.js';
import Modal from './modal.jsx';
// import log from '../../lib/logging';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
// import Cookies from 'js-cookie';

const { Provider, connect } = ReactRedux;

const mapStateToProps = (state) => ({
  start: state.draftGroupPlayers.sport,
  entries: state.contestPoolEntries,
});

const mapDispatchToProps = (dispatch) => ({
  fetchContestPoolEntries: () => dispatch(fetchContestPoolEntries()),
});

const LiveModal = React.createClass({
  propTypes: {
    onClose: React.PropTypes.func,
    showCloseButton: React.PropTypes.bool,
    entries: React.PropTypes.object,
    fetchContestPoolEntries: React.PropTypes.func,
  },
  defaultProps: {
    showCloseButton: true,
  },
  componentWillMount() {
    // TODO: will need to check cookie id with current event
    this.props.fetchContestPoolEntries();
    // log.info({`{ $this.props.entries }`});

    this.setState({
      isOpen: false,
    });

    // log.info({entries});
  },
  onClose() {
    this.setState({
      isOpen: false,
    });
    AppStateStore.modalClosed();
  },
  isOpen() {
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
          <header className="cmp-modal__header">hello world</header>
          <div className="cmp-draft-group-select">
            <p>hello world</p>
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
