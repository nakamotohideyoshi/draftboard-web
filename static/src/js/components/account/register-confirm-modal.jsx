import React from 'react';
import Modal from '../modal/modal.jsx';
import AppStateStore from '../../stores/app-state-store.js';


/**
 * When a user attempts to enter a contest, prompt them to confirm.
 */
const RegisterConfirmModal = React.createClass({

  propTypes: {
    confirmEntry: React.PropTypes.func.isRequired,
    cancelEntry: React.PropTypes.func.isRequired,
    isOpen: React.PropTypes.bool,
    children: React.PropTypes.element.isRequired,
    titleText: React.PropTypes.string.isRequired,
  },


  getInitialState() {
    return {
      isOpen: this.props.isOpen,
    };
  },


  // If the parent component tells us the modal should be closed via prop change, close it.
  // The parent can also call this components 'close()' method directly.
  componentWillReceiveProps(nextProps) {
    this.setState({ isOpen: nextProps.isOpen });
    AppStateStore.modalOpened();
  },


  // Open the modal.
  open() {
    this.setState({ isOpen: true });
  },


  // This gets called when the user requests to close the modal.
  close() {
    // close the modal.
    this.setState({ isOpen: false });
    AppStateStore.modalClosed();
  },


  // When the user clicks the 'ok' button.
  handleConfirmEntry() {
    // confirm entry via the provided function.
    this.props.confirmEntry();
    this.close();
  },


  // When the user clicks the 'cancel' button.
  handleCancelEntry(event) {
    event.preventDefault();
    // confirm entry via the provided function.
    this.props.cancelEntry();
    this.close();
  },


  render() {
    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className="cmp-modal--register-confirm"
        showCloseBtn={false}
      >
        <div>
          <div className="cmp-register-confirm-modal">
            <div className="content">
              <div className="content-inner">
                <div className="top-icon" />
                <div className="title">{this.props.titleText}</div>
                <div className="text-content">{this.props.children}</div>
              </div>

              <div className="controls">
                <div
                  className="button button--gradient button--lrg-len ok-button"
                  onClick={this.handleConfirmEntry}
                >
                  SIGN UP
                </div>
                <a
                  href="#"
                  className="no-thanks"
                  onClick={this.handleCancelEntry}
                >
                  No thanks
                </a>
              </div>
            </div>
          </div>

        </div>
      </Modal>
    );
  },

});


module.exports = RegisterConfirmModal;
