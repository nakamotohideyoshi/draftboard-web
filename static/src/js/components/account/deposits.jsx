import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
// import DepositsPayments from './subcomponents/deposits-payments.jsx';
import { deposit } from '../../actions/payments';
import { setupOnDomElementId } from '../../lib/paypal/paypal';
import log from '../../lib/logging';


const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    user: state.user.info,
    payPalNonce: state.payments.payPalNonce,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    deposit: (postData) => dispatch(deposit(postData)),
  };
}


const Deposits = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    deposit: React.PropTypes.func.isRequired,
    payPalNonce: React.PropTypes.string.isRequired,
  },


  componentWillMount() {
    setupOnDomElementId();
  },


  /**
   * When input quickDeposit is click, populate the input field with its value
   * @param  {Object} event
   */
  syncDepositValues(event) {
    const depositInput = document.getElementById('deposit');
    depositInput.value = event.target.value;
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
  },


  submitDeposit() {
    event.preventDefault();
    if (this.props.payPalNonce !== '') {
      // gather post data
      this.props.deposit(this.props.payPalNonce, 1);
    } else {
      log.error('nonce is blank!');
    }
  },


  render() {
    const depositOptions = ['25', '50', '100', '250', '500'];

    const quckDeposits = depositOptions.map((amount) => {
      const dolarPrepended = '$'.concat(amount);
      return (
        <li key={amount}>
          <input
            type="radio"
            name="quickDeposit"
            value={amount}
            id={dolarPrepended}
            onClick={this.syncDepositValues}
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
                className="form-field__text-input"
                type="text"
                name="deposit"
                id="deposit"
                placeholder="700"
                onChange={this.uncheckQuickDeposits}
                required
              />
            </span>
          </div>

          </fieldset>
        </div>
        <h5>PayPal</h5>
        <div id="paypal-container">
          PP Container
        </div>

        <input onClick={this.submitDeposit} type="submit" className="button button--flat-alt1" value="Deposit" />
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
