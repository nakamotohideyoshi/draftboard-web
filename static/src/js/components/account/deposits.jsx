import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { deposit } from '../../actions/payments';
import { setupBraintree, beginPaypalCheckout } from '../../lib/paypal/paypal';
import log from '../../lib/logging';
import {
  verifyLocation,
  fetchUser, verifyIdentity, checkUserIdentityVerificationStatus } from '../../actions/user';
import { addMessage, removeMessage } from '../../actions/message-actions.js';
import debounce from 'lodash/debounce';
import classNames from 'classnames';
import PubSub from 'pubsub-js';
const { Provider, connect } = ReactRedux;
const depositOptions = ['25', '50', '100', '250', '500'];
import RestrictedLocationConfirmModal from './restricted-location-confirm-modal';
import IdentityVerificationModal from './identity-verification-modal';


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
    // As soon as the compenent boots up, setup braintree.
    // This will fetch the client token.
    this.props.setupBraintree((paypalInstance) => {
      this.setState({ paypalInstance });
      this.enablePaypalButton();
    });
    // First check if the user's location is valid. they will be prompted and warned if not.
    this.props.verifyLocation();
    // Listen for a succesful deposit message.
    // When we find out the deposit is a success, reset the form.
    PubSub.subscribe('account.depositSuccess', () => this.resetForm());
  },


  componentWillReceiveProps(nextProps) {
    // If we had a nonce token, but now we don't, remove any paypal buttons.
    // This will happen if the api request to deposit fails. We have to assume
    // that when we make the deposit request that the nonce has been used and
    // that a new one needs to be fetched.
    if (this.props.payPalNonce && !nextProps.payPalNonce) {
      this.resetForm();
    }
  },


  getButtonText() {
    // We don't have a client token yet.
    if (!this.props.payPalClientToken) {
      return 'Initializing...';
    }
    // We are waiting on a response from our server.
    if (this.props.isDepositing) {
      return 'Depositing...';
    }
    // We have a deposit amount and can display it
    if (this.state.amount) {
      return `Deposit $${this.state.amount} with PayPal`;
    }
    // The form is in the starting state.
    return 'Choose an Amount';
  },


  doHaveNonce() {
    return !!this.props.payPalNonce;
  },


  doHaveClientToken() {
    return !!this.props.payPalClientToken;
  },


  resetForm() {
    this.setState({ amount: '' });
    // Reset text input
    this.refs.textInput.value = '';
    const radios = document.querySelectorAll('.depositRadio');
    // Uncheck all the radio inputs.
    for (let i = 0; i < radios.length; ++i) {
      radios[i].checked = false;
    }
    // Enable the paypal button click event.
    this.enablePaypalButton();
  },


  enablePaypalButton() {
    this.setState({ paypalButtonEnabled: true });
  },


  disablePaypalButton() {
    this.setState({ paypalButtonEnabled: false });
  },


  handleButtonClick() {
    if (this.state.paypalButtonEnabled) {
      store.dispatch(removeMessage('limit error'));
      log.info('Initiating Paypal checkout.');
      this.checkoutInit();
    } else {
      store.dispatch(addMessage({
        header: 'Failed',
        content: 'Sorry but you have exceeded your limit',
        level: 'warning',
        id: 'limit error',
      }));
      log.warn('Ignoring button click.');
    }
  },


  /**
   * Beging the paypal checkout process. This opens up a Paypal popup.
   *
   */
  checkoutInit() {
    // We have begun a checkout, disable the button. It will be re-enabled when
    // the user closes the window. or the process fails.
    this.disablePaypalButton();
    this.props.beginPaypalCheckout({
      paypalInstance: this.state.paypalInstance,
      amount: this.state.amount,
      onClosed: () => {
        // The popup was closed, re-enable the button.
        this.enablePaypalButton();
      },
      onPaymentMethodReceived: (nonce, amount) => {
        // The user succesfullly completed the paypal checkout. Now we can send
        // our authorization token to the server for the transaction to occur.
        log.info('onPaymentMethodReceived()', nonce);
        if (!this.props.isDepositing) {
          this.props.deposit(nonce, amount);
        }
      },
    });
  },


  handleRadioClick(event) {
    if (this.doHaveNonce()) {
      log.warn('not changing values, we already have a nonce for the current value.');
      return;
    }
    // Update the textarea value.
    this.refs.textInput.value = event.target.value;
    this.handleTextInputChange(event);
    // update state amount and add button
    this.setState(
      { amount: event.target.value }
    );
  },


  handleTextInputChange(event) {
    if (this.props.depositLimit) {
      if ((this.props.depositSum + Number(this.refs.textInput.value)) > this.props.depositLimit) {
        store.dispatch(addMessage({
          header: 'Cannot Deposit',
          content: 'Sorry but you have exceeded your deposit limit',
          level: 'warning',
          id: 'limit error',
        }));

        this.disablePaypalButton();
      } else {
        this.enablePaypalButton();
      }
    }
    this.uncheckQuickDeposits();
    this.handleTextInputBlur(event);
  },


  handleTextInputBlur() {
    if (this.doHaveNonce()) {
      log.warn('not changing values, we already have a nonce for the current value.');
      return;
    }

    // update state amount and add button
    this.setState(
      { amount: this.refs.textInput.value }
    );
  },


  /**
   * Uncheck quickDeposits options if any is selected (when input field is modified directly)
   * @return null (DOM modifications)
   */
  uncheckQuickDeposits() {
    const quickDeposits = document.querySelectorAll("input[type][name='quickDeposit']");
    for (let i = 0; i < quickDeposits.length; i++) {
      quickDeposits[i].checked = false;
    }

    this.setState({ amount: this.refs.textInput.value });
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
    if (!this.props.user.identity_verified && this.props.user.hasFetched) {
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
    const depositButtonClasses = classNames('button button--flat-alt1');
    // If we have a nonce, or if we have an outstanding deposit request, disable the button.
    const buttonIsDisabled = (this.doHaveNonce() || !this.state.amount || this.props.isDepositing);
    // Create the list of quick deposit amounts.
    const quckDeposits = depositOptions.map((amount) => {
      const dolarPrepended = '$'.concat(amount);
      return (
        <li key={amount}>
          <input
            className="depositRadio"
            type="radio"
            name="quickDeposit"
            value={amount}
            id={dolarPrepended}
            onClick={this.handleRadioClick}
            disabled={this.doHaveNonce()}
          />
          <label htmlFor={dolarPrepended}>{dolarPrepended}</label>
        </li>
      );
    });

    return (
      <div className="cmp-account-deposits">
        <div className="form">
          <fieldset className="form__fieldset">

            <div className="form-field">
              <label className="form-field__label" htmlFor="deposit">Quick Deposit</label>

              <ul className="radio-button-list--quick-deposit">
                {quckDeposits}
              </ul>
            </div>

            <div className="form-field">
              <label className="form-field__label" htmlFor="amount">Other Amount</label>
              <span className="input-symbol-dollar">
                <input
                  ref="textInput"
                  className="form-field__text-input"
                  type="number"
                  name="deposit"
                  id="deposit"
                  placeholder="Enter a deposit amount"
                  onChange={debounce(this.handleTextInputChange, 500)}
                  onBlur={this.handleTextInputBlur}
                  disabled={this.doHaveNonce()}
                  required
                />
              </span>
            </div>

          </fieldset>
        </div>

        <div id="paypal-container" ref="paypal-container">
          <button
            disabled={buttonIsDisabled}
            id="paypal-button"
            ref="paypal-button"
            data-amount={this.state.amount}
            className={depositButtonClasses}
            onClick={this.handleButtonClick}
          >{ this.getButtonText() }</button>
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
