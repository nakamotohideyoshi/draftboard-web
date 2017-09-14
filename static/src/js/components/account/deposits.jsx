import Raven from 'raven-js';
import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { deposit, fetchDepositForm, gidxSessionComplete } from '../../actions/payments';
import log from '../../lib/logging';
import { verifyLocation, fetchUser, verifyIdentity,
  checkUserIdentityVerificationStatus } from '../../actions/user';
const { Provider, connect } = ReactRedux;
import RestrictedLocationConfirmModal from './restricted-location-confirm-modal';
import IdentityVerificationModal from './identity-verification-modal';


function mapStateToProps(state) {
  return {
    user: state.user.user,
    isDepositing: state.payments.isDepositing,
    depositSum: state.user.cashBalance.depositSum,
    depositLimit: state.user.cashBalance.depositLimit,
    userLocation: state.user.location,
    identityFormInfo: state.user.identityFormInfo,
    gidxFormInfo: state.user.gidxFormInfo,
    gidxPaymentForm: state.payments.gidx.paymentForm,
    merchantSessionId: state.payments.gidx.paymentForm.merchantSessionId,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchUser: () => dispatch(fetchUser()),
    deposit: (nonce, amount) => dispatch(deposit(nonce, amount)),
    verifyLocation: () => dispatch(verifyLocation()),
    verifyIdentity: (postData) => dispatch(verifyIdentity(postData)),
    checkUserIdentityVerificationStatus: (merchantSessionID) => dispatch(
      checkUserIdentityVerificationStatus(merchantSessionID)),
    fetchDepositForm: () => dispatch(fetchDepositForm()),
    gidxSessionComplete: (sessionId) => dispatch(gidxSessionComplete(sessionId)),
  };
}


const Deposits = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    deposit: React.PropTypes.func.isRequired,
    isDepositing: React.PropTypes.bool.isRequired,
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
    gidxSessionComplete: React.PropTypes.func.isRequired,
    merchantSessionId: React.PropTypes.string,
  },


  componentDidMount() {
    const self = this;
    // These functions are needed for the GIDX embed script.
    window.gidxServiceSettings = () => {
      window.gidxBuildSteps = false;
      // this is the dom object (div) where the cashier/registration service should be embedded
      // son the page.
      window.gidxContainer = '#GIDX_ServiceContainer';
    };

    window.gidxErrorReport = (error, errorMsg) => {
      log.error('gidxErrorReport', error, errorMsg);
      // send errors to Sentry.
      Raven.captureMessage(errorMsg, {
        error,
        level: 'error',
      });
    };

    // This never works. wtf.
    window.gidxNextStep = () => {
      log.info('gidxNextStep');
    };

    window.gidxServiceStatus = (service, action, json) => {
      log.info('gidxServiceStatus', service, action, json);

      // The trasnaction is complete. Tell our server to fetch the details.
      if (service === 'cashierComplete-plate' && action === 'start') {
        self.props.gidxSessionComplete(self.props.merchantSessionId);
      }
    };

    this.props.fetchUser();
    this.props.fetchDepositForm();

    // First check if the user's location is valid. they will be prompted and warned if not.
    this.props.verifyLocation();
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


  renderPaymentFormContainer() {
    // If we have a payment form, render the html that the form needs to display itself.
    if (this.props.gidxPaymentForm.formEmbed) {
      return (
        <div>
          <div id="DepositAmountDisplay"></div>
          <div id="GIDX_ServiceContainer"></div>

          <div id="GIDX">
            <div ref="GIDX_embed">
              <div className="loading-placeholder" data-gidx-script-loading="true">
                Initializing secure deposit process...
              </div>

              <div
                id="GIDX_embed_hidden"
                ref="originalEmbed"
                dangerouslySetInnerHTML={{ __html: this.props.gidxPaymentForm.formEmbed }}
              ></div>
            </div>
          </div>
        </div>
      );
    }

    return (<div></div>);
  },

  render() {
    return (
      <div className="cmp-account-deposits">
        { this.renderPaymentFormContainer() }
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
