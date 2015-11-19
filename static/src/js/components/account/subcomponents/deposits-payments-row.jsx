"use strict";
var React = require('react');

var ModalRemovePaymentMethod = require('./modal-remove-payment-method.jsx');
var AccountActions = require('../../../actions/account-actions');


/**
 * Renders a single PaymentMethod with actions connected to it (set as default / remove)
 */
var DepositsPaymentsRow = React.createClass({

  propTypes: {
    method: React.PropTypes.object.isRequired
  },

  openModal: function(event) {
    event.preventDefault();
    this.refs.removePaymentMethodModal.open();
  },

  /**
   * Change user's default payment method to this one
   */
  setAsDefault: function(event) {
    event.preventDefault();
    AccountActions.setDefaultPaymentMethod(this.props.method.id);
  },

  /**
   * Remove this payment method from user's available payment methods
   */
  removePaymentMethod: function(event) {
    event.preventDefault();
    AccountActions.removePaymentMethod(this.props.method.id);
  },

  render: function() {
    // select the proper icon for this payment method (visa / mastercard / american express etc.)
    var iconClass = "creditcard-icon__"  + this.props.method.type;

    return (
        <li>
          <span className={iconClass}></span>
          <p className="details">Ending in {this.props.method.ending} expire {this.props.method.expires}</p>
          <p className="is-default">
          { this.props.method.default &&
            '(default)'
          }
          { !this.props.method.default &&
            <a href="#" onClick={this.setAsDefault} className='setdefault__creditcard'>Set as Default</a>
          }
          </p>

          <span>
            <a href="#" className="remove__creditcard" onClick={this.openModal}></a>
            <ModalRemovePaymentMethod
              ref="removePaymentMethodModal"
              onConfirm={this.removePaymentMethod} />
          </span>
        </li>
    );
  }
});


module.exports = DepositsPaymentsRow;
