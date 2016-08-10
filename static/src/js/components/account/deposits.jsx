import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { deposit } from '../../actions/payments';
import { setupPaypalButton } from '../../lib/paypal/paypal';
import log from '../../lib/logging';
import { fetchPayPalClientTokenIfNeeded } from '../../actions/payments';
import debounce from 'lodash/debounce';
import classNames from 'classnames';
import PubSub from 'pubsub-js';

const { Provider, connect } = ReactRedux;
const depositOptions = ['25', '50', '100', '250', '500'];


function mapStateToProps(state) {
  return {
    user: state.user.info,
    payPalNonce: state.payments.payPalNonce,
    isDepositing: state.payments.isDepositing,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchPayPalClientTokenIfNeeded: () => dispatch(fetchPayPalClientTokenIfNeeded()),
    deposit: (nonce, amount) => dispatch(deposit(nonce, amount)),
    setupPaypalButton,
  };
}


const Deposits = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    deposit: React.PropTypes.func.isRequired,
    isDepositing: React.PropTypes.bool.isRequired,
    payPalNonce: React.PropTypes.string,
    fetchPayPalClientTokenIfNeeded: React.PropTypes.func.isRequired,
    setupPaypalButton: React.PropTypes.func.isRequired,
  },


  getInitialState() {
    return {
      amount: null,
    };
  },


  componentWillMount() {
    PubSub.subscribe('account.depositSuccess', () => this.resetForm());
    // Once we know it will mount, fetch a paypal client token from our server.
    // We need this in order to get a nonce from the user.
    this.props.fetchPayPalClientTokenIfNeeded();
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


  doHaveNonce() {
    return !!this.props.payPalNonce;
  },


  resetForm() {
    // Remove Paypal button.
    this.refs['paypal-container'].innerHTML = '';
    this.setState({ amount: '' });
    // Reset text input
    this.refs.textInput.value = '';
    const radios = document.querySelectorAll('.depositRadio');
    // Uncheck all the radio inputs.
    for (let i = 0; i < radios.length; ++i) {
      radios[i].checked = false;
    }
  },


  removeAllButLastElement(nodeList) {
    if (nodeList.length > 1) {
      for (let i = 0; i < nodeList.length - 1; i++) {
        nodeList[i].remove();
      }
    }
  },


  addPaypalButton(amount) {
    // remove any existing paypal buttons.
    this.refs['paypal-container'].innerHTML = '';

    // Note: this is a promise.
    this.props.setupPaypalButton(
      'paypal-container',
      amount,
      // onReady
      () => {
        // Because of the async nature of the paypal integration, sometimes if the user thrash
        // clicks we end up with multiple buttons. Buttons are added at the end of the container, so
        // we can just remove all but that last placed set.
        this.removeAllButLastElement(document.querySelectorAll('#braintree-paypal-loggedin'));
        this.removeAllButLastElement(document.querySelectorAll('#braintree-paypal-loggedout'));
      }
    );
  },


  handleRadioClick(event) {
    if (this.doHaveNonce()) {
      log.warn('not changing values, we already have a nonce for the current value.');
      return;
    }
    // Update the textarea value.
    this.refs.textInput.value = event.target.value;
    // update state amount and add button
    this.setState(
      { amount: event.target.value },
      this.addPaypalButton(event.target.value)
    );
  },


  handleTextInputChange(event) {
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
      { amount: this.refs.textInput.value },
      this.addPaypalButton(this.refs.textInput.value)
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


  submitDeposit() {
    event.preventDefault();
    if (this.doHaveNonce() && !this.props.isDepositing) {
      // gather post data
      this.props.deposit(this.props.payPalNonce, this.state.amount);
    } else {
      log.warn('Click ignored. Either nonce is blank, or we are currently depositing.');
    }
  },


  render() {
    // If we don't have a nonce, or if we have an outstanding deposit request, disable the button.
    const depositButtonClassses = classNames(
      'button button--flat-alt1',
      { 'button--disabled': !this.doHaveNonce() || this.props.isDepositing }
    );

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
      <div>
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
                  type="text"
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

        <div id="paypal-container" ref="paypal-container"></div>

        <input onClick={this.submitDeposit} type="submit" className={depositButtonClassses} value="Deposit" />
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


export default DepositsConnected;
