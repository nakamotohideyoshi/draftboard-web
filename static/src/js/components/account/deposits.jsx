import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { updateUserAddress } from '../../actions/user';
// import DepositsAddPaymentMethod from './subcomponents/deposits-add-payment-method.jsx';
import DepositsPayments from './subcomponents/deposits-payments.jsx';
import SettingsAddress from './subcomponents/settings-address.jsx';

import {
  fetchPaymentMethods,
  addPaymentMethod,
  setPaymentMethodDefault,
  removePaymentMethod,
  deposit,
} from '../../actions/payments';


const { Provider, connect } = ReactRedux;

function mapStateToProps(state) {
  return {
    user: state.user.info,
    addressFormErrors: state.user.addressFormErrors,
    payments: state.payments.payments,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    updateUserAddress: (postData) => dispatch(updateUserAddress(postData)),
    fetchPaymentMethods: () => dispatch(fetchPaymentMethods()),
    addPaymentMethod: (postData) => dispatch(addPaymentMethod(postData)),
    setPaymentMethodDefault: (id) => dispatch(setPaymentMethodDefault(id)),
    removePaymentMethod: (id) => dispatch(removePaymentMethod(id)),
    deposit: (postData) => dispatch(deposit(postData)),
  };
}


const Deposits = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    addressFormErrors: React.PropTypes.object.isRequired,
    updateUserAddress: React.PropTypes.func.isRequired,

    payments: React.PropTypes.array.isRequired,
    fetchPaymentMethods: React.PropTypes.func.isRequired,

    addPaymentMethod: React.PropTypes.func.isRequired,
    setPaymentMethodDefault: React.PropTypes.func.isRequired,
    removePaymentMethod: React.PropTypes.func.isRequired,
    deposit: React.PropTypes.func.isRequired,
  },


  componentWillMount() {
    this.props.fetchPaymentMethods();
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


  submitDeposit(event) {
    event.preventDefault();
    // gather post data
    this.props.deposit({});
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

          <DepositsPayments
            payments={this.props.payments}
            onSetDefault={this.props.setPaymentMethodDefault}
            onRemovePaymentMethod={this.props.removePaymentMethod}
          />

          <input type="submit" className="button button--flat-alt1" value="Deposit" />

          </fieldset>
        </div>

        <SettingsAddress
          info={this.props.user}
          errors={{}}
          onHandleSubmit={this.props.updateUserAddress}
        />

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
