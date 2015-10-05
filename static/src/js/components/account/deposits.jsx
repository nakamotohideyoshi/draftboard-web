"use strict";

var React = require('react');
var Reflux = require('reflux');
var renderComponent = require('../../lib/render-component');

var AccountActions = require('../../actions/account-actions');
var AccountStore = require('../../stores/account-store');

var DepositsAddPaymentMethod = require('./subcomponents/deposits-add-payment-method.jsx');
var DepositsPayments = require('./subcomponents/deposits-payments.jsx');

var SettingsAddress = require('./subcomponents/settings-address.jsx');


/**
 * Renders the DepositsSection in the account section.
 */
var Deposits = React.createClass({

  mixins: [
    Reflux.connect(AccountStore)
  ],

  getInitialState: function() {
    AccountActions.getPaymentMethods();
    return {
      'paymentMethods': AccountStore.data.paymentMethods,
      'errors': AccountStore.data.depositFormErrors
    };
  },

  /**
   * When input quickDeposit is click, populate the input field with its value
   * @param  {Object} event
   */
  syncDepositValues: function(event) {
    var depositInput = document.getElementById('deposit');
    depositInput.value = event.target.value;
  },

  /**
   * Uncheck quickDeposits options if any is selected (when input field is modified directly)
   * @return null (DOM modifications)
   */
  uncheckQuickDeposits: function() {
    var quickDeposits = document.querySelectorAll("input[type][name='quickDeposit']");
    for (var i = 0; i < quickDeposits.length; i++) {
      quickDeposits[i].checked = false;
    }
  },

  submitDeposit: function(event) {
    event.preventDefault();
    AccountActions.deposit();
  },

  render: function() {

    var depositOptions = ['25', '50', '100', '250', '500'];

    var quckDeposits = depositOptions.map(function(amount) {
      var dolarPrepended = '$'.concat(amount);
      return (
        <li>
          <input
            type="radio"
            name="quickDeposit"
            value={amount}
            id={dolarPrepended}
            onClick={this.syncDepositValues} />
          <label htmlFor={dolarPrepended}>{dolarPrepended}</label>
        </li>
      );
    }.bind(this));

    var csrftokken = document.cookie.match(/csrftoken=(.*?)(?:$|;)/)[1];

    return (
      <div>
        <form className="form" method="post" onSubmit={this.submitDeposit}>
          <input type="hidden" name="csrfmiddlewaretoken" value={csrftokken} />

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
                required />
            </span>
          </div>

          <DepositsPayments methods={this.state.paymentMethods} />
          <DepositsAddPaymentMethod />
          <input type="submit" className="button--medium" value="Deposit" />

          </fieldset>
        </form>

        <SettingsAddress />

      </div>
    );
  }

});


renderComponent(<Deposits />, '#account-deposits');


module.exports = Deposits;
