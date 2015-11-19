"use strict";

var React = require('react');
var renderComponent = require('../../lib/render-component');
var AccountActions = require('../../actions/account-actions');
var AccountStore = require('../../stores/account-store');

var SSNMaskedInput = require('../form-field/ssn.jsx');


var Withdrawals = React.createClass({

  getInitialState: function() {

    return {
      'errors': AccountStore.data.withdrawFormErrors
    };
  },

  /**
   * Withdraw the submitted amount.
   * If errors from backend come, populate the form accordingly
   */
  withdrawAmount: function(event) {
    event.preventDefault();
    AccountActions.withdraw();
  },

  render: function() {

    var csrftokken = document.cookie.match(/csrftoken=(.*?)(?:$|;)/)[1];

    return (
      <div>
        <form className="form" method="post" onSubmit={this.withdrawAmount}>

        <input type="hidden" name="csrfmiddlewaretoken" value={csrftokken} />

        <fieldset className="form__fieldset">
          <div className="form-field">
            <label className="form-field__label" htmlFor="amount">
              Withdraw Amount
            </label>

            <span className="input-symbol-dollar">
              <input
                className="form-field__text-input"
                type="text"
                name="amount"
                id="amount"
                placeholder="700"
                required
              />
            </span>
          </div>

          <div className="form-field">
            <label className="form-field__label form-field__label--twoline" htmlFor="ssn">
              SSN for Taxes<br />(1099 Misc.)
            </label>
            <SSNMaskedInput />
          </div>

          <div className="form-field form-field--with-help">
            <label className="form-field__label" htmlFor="notifications">Withdraw Method</label>
            <div className="form-field__content">
              <p className="form-field__info">
                You may receive your withdraw thru PayPal or a mailed check. Mailed checks may take between 7-12 business
                days to arrive.
              </p>

              <input className="form-field__text-input" type="email" id="paypal-email" name="paypal-email" placeholder="Paypal associated email address..." />
            </div>
          </div>

          <input type="submit" className="button--medium" value="Withdraw" />
        </fieldset>
        </form>
      </div>
    );
  }

});


renderComponent(<Withdrawals />, '#account-withdrawals');


module.exports = Withdrawals;
