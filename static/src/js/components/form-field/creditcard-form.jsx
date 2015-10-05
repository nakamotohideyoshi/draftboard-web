'use strict';

var React = require('react');
var AccountActions = require('../../actions/account-actions');
var ReactCardFormContainer = require('card-react');


/**
 * CreditcardForm rendering the fancy dynamic, animated creditcard form
 */
var CreditcardForm = React.createClass({
  newPaymentMethod: function(event) {
    event.preventDefault();
    AccountActions.addPaymentMethod();
  },

  render: function() {
    return (
      <ReactCardFormContainer

        container="react-credit-card-animator"

        formInputsNames={
          {
            number: 'CCnumber',
            expiry: 'CCexpiry',
            cvc: 'CCcvc',
            name: 'CCname'
          }
        }
        >

        <div id="react-credit-card-animator" />

        <form className="form form--credit_card_input" onSubmit={this.newPaymentMethod}>
          <div className="form-field">
            <label className="form-field__label" htmlFor="CCnumber">Card number</label>
            <input className="form-field__text-input" type="text" name="CCnumber" id="CCnumber" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="CCname">Cardholders name</label>
            <input className="form-field__text-input" type="text" name="CCname" id="CCname" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="CCexpiry">Expiry Date</label>
            <input className="form-field__text-input" type="text" name="CCexpiry" id="CCexpiry" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="CCcvc">CVV Code</label>
            <input className="form-field__text-input" type="text" name="CCcvc" id="CCcvc" />
          </div>

          <input type="submit" className="button--medium" value="ADD CARD" />
        </form>

      </ReactCardFormContainer>
    );
  }

});


module.exports = CreditcardForm;
