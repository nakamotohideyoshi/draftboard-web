"use strict";

var React = require('react');
var DepositsPaymentsRow = require('./deposits-payments-row.jsx');

/**
 * Renders list of payment methods that this user has available
 */
var DepositsPayments = React.createClass({

  propTypes: {
    methods: React.PropTypes.array.isRequired
  },

  render: function() {
    var paymentMethods = this.props.methods.map(function(method) {
      return (
        <DepositsPaymentsRow key={method.id} method={method} />
      );
    });

    return (
      <div className="form-field">
        <label className="form-field__label" htmlFor="amount">Payment Method</label>
        <div className="form-field__content">

        <ul className="creditcard-listing">
          {paymentMethods}
        </ul>

        </div>
      </div>
    );
  }

});


module.exports = DepositsPayments;
