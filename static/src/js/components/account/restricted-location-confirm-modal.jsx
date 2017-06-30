import React from 'react';
import Modal from '../modal/modal.jsx';
import AppStateStore from '../../stores/app-state-store.js';


/**
 * When a user attempts to enter a contest, prompt them to confirm.
 */
const RestrictedLocationConfirmModal = React.createClass({

  propTypes: {
    isOpen: React.PropTypes.bool,
    children: React.PropTypes.element,
    titleText: React.PropTypes.string,
    continueButtonText: React.PropTypes.string,
    showCancelButton: React.PropTypes.bool,
  },

  getDefaultProps() {
    return {
      continueButtonText: 'Continue',
    };
  },


  getInitialState() {
    return {
      isOpen: this.props.isOpen,
      hasBeenDismissed: false,
      showCancelButton: true,
    };
  },


  // If the parent component tells us the modal should be closed via prop change, close it.
  // The parent can also call this components 'close()' method directly.
  componentWillReceiveProps(nextProps) {
    // If it's already been dismissed, don't ever open it again.
    if (!this.state.hasBeenDismissed) {
      this.setState({ isOpen: nextProps.isOpen });
      AppStateStore.modalOpened();
    }
  },


  // Open the modal.
  open() {
    // If it's already been dismissed, don't ever open it again.
    if (!this.state.hasBeenDismissed) {
      this.setState({ isOpen: true });
    }
  },


  // This gets called when the user requests to close the modal.
  close() {
    // close the modal.
    this.setState({ isOpen: false, hasBeenDismissed: true });
    AppStateStore.modalClosed();
  },


  renderCancelButton() {
    if (this.props.showCancelButton) {
      return (
        <a
          href="/"
          className="no-thanks"
        >No thanks</a>
      );
    }
    return '';
  },


  render() {
    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className="cmp-modal--restricted-location-confirm"
        showCloseBtn={false}
      >
        <div>
          <div className="cmp-restricted-location-confirm">
            <div className="content">
              <div className="content-inner">
                <div className="top-icon" />
                <div className="title">{this.props.titleText}</div>
                <div className="text-content">{this.props.children}</div>
              </div>

              <div className="controls">
                <div
                  className="button button--gradient button--lrg-len ok-button"
                  onClick={this.close}
                >
                  {this.props.continueButtonText}
                </div>
                {this.renderCancelButton()}
              </div>
            </div>
          </div>

        </div>
      </Modal>
    );
  },

});


export default RestrictedLocationConfirmModal;
