import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import AppStateStore from '../../stores/app-state-store.js';
import Modal from './modal.jsx';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
// import Cookies from 'js-cookie';

const { Provider, connect } = ReactRedux;

const mapStateToProps = (state) => ({
  start: state.draftGroupPlayers.sport,
});

const LiveModal = React.createClass({
  defaultProps: {
    showCloseButton: true,
  },
  propTypes: {
    // sport: React.PropTypes.string.required,
    onClose: React.PropTypes.func,
    showCloseButton: React.PropTypes.bool,
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
  componentWillMount() {
    this.setState({
      isOpen: false,
    });
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
  mapStateToProps
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
