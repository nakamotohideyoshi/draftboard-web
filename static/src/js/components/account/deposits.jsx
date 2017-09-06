import Raven from 'raven-js';
import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { deposit, fetchDepositForm } from '../../actions/payments';
import { setupBraintree, beginPaypalCheckout } from '../../lib/paypal/paypal';
import log from '../../lib/logging';
import {
  verifyLocation,
  fetchUser, verifyIdentity, checkUserIdentityVerificationStatus } from '../../actions/user';

import PubSub from 'pubsub-js';
const { Provider, connect } = ReactRedux;
import RestrictedLocationConfirmModal from './restricted-location-confirm-modal';
import IdentityVerificationModal from './identity-verification-modal';


// These functions are needed for the GIDX embed script.
window.gidxServiceSettings = () => {
  window.gidxBuildSteps = true;
  // this is the dom object (div) where the cashier/registration service should be embedded
  // son the page.
  window.gidxContainer = '#GIDX_ServiceContainer';
};

window.gidxServiceStatus = (service, action, json) => {
  log.info(service, action, json);
};

window.gidxErrorReport = (error, errorMsg) => {
    // Error messages will be sent here by the GIDX Client Side Service
  log.error('======= gidxErrorReport =========');
  // send errors to Sentry.
  Raven.captureMessage(errorMsg, {
    error,
    level: 'error',
  });
  log.error(error, errorMsg);
};

window.gidxNextStep = () => {
  log.info('gidxNextStep');
};


function mapStateToProps(state) {
  return {
    user: state.user.user,
    payPalNonce: state.payments.payPalNonce,
    payPalClientToken: state.payments.payPalClientToken,
    isDepositing: state.payments.isDepositing,
    depositSum: state.user.cashBalance.depositSum,
    depositLimit: state.user.cashBalance.depositLimit,
    userLocation: state.user.location,
    identityFormInfo: state.user.identityFormInfo,
    gidxFormInfo: state.user.gidxFormInfo,
    gidxPaymentForm: state.payments.gidx.paymentForm,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchUser: () => dispatch(fetchUser()),
    deposit: (nonce, amount) => dispatch(deposit(nonce, amount)),
    setupBraintree: (callback) => setupBraintree(callback),
    beginPaypalCheckout: (options) => beginPaypalCheckout(options),
    verifyLocation: () => dispatch(verifyLocation()),
    verifyIdentity: (postData) => dispatch(verifyIdentity(postData)),
    checkUserIdentityVerificationStatus: (merchantSessionID) => dispatch(
      checkUserIdentityVerificationStatus(merchantSessionID)),
    fetchDepositForm: () => dispatch(fetchDepositForm()),
  };
}


const Deposits = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    deposit: React.PropTypes.func.isRequired,
    isDepositing: React.PropTypes.bool.isRequired,
    payPalNonce: React.PropTypes.string,
    payPalClientToken: React.PropTypes.string,
    setupBraintree: React.PropTypes.func.isRequired,
    beginPaypalCheckout: React.PropTypes.func.isRequired,
    verifyLocation: React.PropTypes.func.isRequired,
    userLocation: React.PropTypes.object.isRequired,
    verifyIdentity: React.PropTypes.func.isRequired,
    fetchUser: React.PropTypes.func.isRequired,
    depositSum: React.PropTypes.number.isRequired,
    depositLimit: React.PropTypes.number.isRequired,
    identityFormInfo: React.PropTypes.object.isRequired,
    gidxFormInfo: React.PropTypes.object.isRequired,
    gidxPaymentForm: React.PropTypes.object.isRequired,
    fetchDepositForm: React.PropTypes.func.isRequired,
    checkUserIdentityVerificationStatus: React.PropTypes.func.isRequired,
  },


  getInitialState() {
    return {
      amount: null,
      paypalInstance: {},
      paypalButtonEnabled: false,
    };
  },


  componentWillMount() {
    this.props.fetchUser();
    this.props.fetchDepositForm();

    // First check if the user's location is valid. they will be prompted and warned if not.
    this.props.verifyLocation();
    // Listen for a succesful deposit message.
    // When we find out the deposit is a success, reset the form.
    PubSub.subscribe('account.depositSuccess', () => this.resetForm());
  },

  componentDidUpdate(prevProps) {
    // If it's the first time we've recieved the form embed...
    if (!prevProps.gidxPaymentForm.formEmbed && this.props.gidxPaymentForm.formEmbed) {
      // This is some hack-ass shit.
      // In order to embed and run a script, you have to do it this way.
      const scriptTag = document.querySelector('#GIDX script');
      const newScriptTag = document.createElement('script');

      newScriptTag.type = 'text/javascript';
      newScriptTag.src = scriptTag.src;

      for (let i = 0; i < scriptTag.attributes.length; i++) {
        const a = scriptTag.attributes[i];
        newScriptTag.setAttribute(a.name, a.value);
      }
      this.refs.originalEmbed.remove();
      this.refs.GIDX_embed.append(newScriptTag);
    }
  },

  renderLocationConfirmModalIfNeeded() {
    // If we know that they do not have a verified identity.
    if (
      this.props.userLocation.hasAttemptedToVerify &&
      !this.props.userLocation.isLocationVerified
    ) {
      // Show a modal warning them that they will not be able to do some things.
      return (
          <RestrictedLocationConfirmModal
            isOpen
            titleText="Location Unavailable"
            continueButtonText="Continue"
          >
            <div>{this.props.userLocation.message || 'Your location could not be verified.'}</div>
          </RestrictedLocationConfirmModal>
      );
    }
    // By default do not show confirm modal.
    return '';
  },


  renderIdentityVerificationModalIfNeeded() {
    // If the user's identity is not verified (and we've checked) OR if we've already
    // tried to verify them.
    if (
      !this.props.user.identity_verified && this.props.user.hasFetched ||
      this.props.identityFormInfo.hasMadeBasicAttempt
    ) {
      return (
        <IdentityVerificationModal
          isOpen
          identityFormInfo={this.props.identityFormInfo}
          gidxFormInfo={this.props.gidxFormInfo}
          verifyIdentity={this.props.verifyIdentity}
          user={this.props.user}
          checkUserIdentityVerificationStatus={this.props.checkUserIdentityVerificationStatus}
        />
      );
    }

    return '';
  },


  render() {
    return (
      <div className="cmp-account-deposits">

        <div id="DepositAmountDisplay"></div>
        <div id="GIDX_ServiceContainer"></div>

        <div id="GIDX">
          <div ref="GIDX_embed">
            <div data-gidx-script-loading="true">Loading...</div>

            <div
              id="GIDX_embed_hidden"
              ref="originalEmbed"
              dangerouslySetInnerHTML={{ __html: this.props.gidxPaymentForm.formEmbed }}
            ></div>
          </div>
        </div>

        { this.renderIdentityVerificationModalIfNeeded() }
        { this.renderLocationConfirmModalIfNeeded() }
      </div>
    );
  },

});


const DepositsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Deposits);


renderComponent(
  <Provider store={store}>
    <DepositsConnected />
  </Provider>, '#account-deposits'
);


// Export the React component.
module.exports = Deposits;
// Export the store-injected ReactRedux component.
export default DepositsConnected;
