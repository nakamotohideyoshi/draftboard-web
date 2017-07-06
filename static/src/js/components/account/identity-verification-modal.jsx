import React from 'react';
import Modal from '../modal/modal.jsx';
import AppStateStore from '../../stores/app-state-store.js';
import IdentityForm from './subcomponents/identity-form';

/**
 * When a user attempts to enter a contest, prompt them to confirm.
 */
const IdentityVerificationModal = React.createClass({

  propTypes: {
    isOpen: React.PropTypes.bool,
    identityFormInfo: React.PropTypes.object.isRequired,
    verifyIdentity: React.PropTypes.func.isRequired,
    user: React.PropTypes.object.isRequired,
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


  // Based on our state, this will render one of the identity forms, or a success message.
  renderContent() {
    // Show a success message.
    if (this.props.user.identity_verified) {
      return (
        <div className="content-verified">
          <h3>Identity Verified!</h3>
          <p>You are now able to <a href="/contests/">enter contests</a> or make a deposit.</p>
          <div
            className="button button--med-len button--tall button--gradient ok-button"
            onClick={this.close}
          >
            Continue
          </div>
        </div>
      );
    }

    // If we've already attempted and failed to ID based on the IdentityForm, show the
    // advanced form.
    if (this.props.identityFormInfo.hasMadeBasicAttempt) {
      return (<p>GIDX drop-in form here.</p>);
    }

    // default to the standard IdentityForm
    return (
      <IdentityForm
        isSending={this.props.identityFormInfo.isSending}
        errors={this.props.identityFormInfo.errors}
        verifyIdentity={this.props.verifyIdentity}
      />
    );
  },


  render() {
    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className="cmp-modal--identity-verification"
        showCloseBtn={false}
      >
        <div>
          <div className="cmp-identity-verification">
            <div className="content">
              <div className="content-inner">
                <div className="text-content">
                  {this.renderContent()}
                </div>
              </div>
            </div>
          </div>
        </div>
      </Modal>
    );
  },

});


export default IdentityVerificationModal;
