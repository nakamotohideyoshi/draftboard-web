'use strict';

var React = require('react');
var ModalAddPaymentMethod = require('./modal-add-payment-method.jsx');


/**
 * Button / Link for adding new payment method connected with that user
 * Opens modal window in which form is provided, for inputting payment method options
 */
var DepositsAddPaymentMethod = React.createClass({

  openModal: function(event) {
    event.preventDefault();
    this.refs.cardModal.open();
  },

  render: function() {
    return (
      <div className="form-field">

        <div className="form-field__content">
          <a
            href="#"
            className="add__paymentmethod"
            onClick={this.openModal}>+ New payment method</a>

          <ModalAddPaymentMethod ref="cardModal" />
        </div>
      </div>
    );
  }
});


module.exports = DepositsAddPaymentMethod;
