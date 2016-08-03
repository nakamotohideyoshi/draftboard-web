import React from 'react';
import DepositsPaymentsRow from './deposits-payments-row.jsx';


const DepositsPayments = (props) => {
  const paymentMethods = props.payments.map((method) => (
      <DepositsPaymentsRow
        key={method.id}
        method={method}
        // onSetDefault={props.onSetDefault}
        onRemovePaymentMethod={props.onRemovePaymentMethod}
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
};

DepositsPayments.propTypes = {
  payments: React.PropTypes.array.isRequired,
  // onSetDefault: React.PropTypes.func.isRequired,
  onRemovePaymentMethod: React.PropTypes.func.isRequired,
};

export default DepositsPayments;
