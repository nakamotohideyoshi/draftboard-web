import React from 'react';
import DepositsPaymentsRow from './deposits-payments-row.jsx';


const DepositsPayments = React.createClass({

  propTypes: {
    payments: React.PropTypes.array.isRequired,
    onSetDefault: React.PropTypes.func.isRequired,
    onRemovePaymentMethod: React.PropTypes.func.isRequired,
  },

  render() {
    const paymentMethods = this.props.payments.map((method) => (
        <DepositsPaymentsRow
          key={method.id}
          method={method}
          onSetDefault={this.props.onSetDefault}
          onRemovePaymentMethod={this.props.onRemovePaymentMethod}
        />
      )
    );

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
  },

});


export default DepositsPayments;
