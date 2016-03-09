import React from 'react';
import ModalRemovePaymentMethod from './modal-remove-payment-method.jsx';


const DepositsPaymentsRow = React.createClass({

  propTypes: {
    method: React.PropTypes.object.isRequired,
    onSetDefault: React.PropTypes.func.isRequired,
    onRemovePaymentMethod: React.PropTypes.func.isRequired,
  },

  openModal(event) {
    event.preventDefault();
    this.refs.removePaymentMethodModal.open();
  },

  handleSetDefault(event) {
    event.preventDefault();
    this.props.onSetDefault(this.props.method.id);
  },

  handleRemovePaymentMethod(event) {
    event.preventDefault();
    this.props.onRemovePaymentMethod(this.props.method.id);
  },

  render() {
    // select the proper icon for this payment method (visa / mastercard / american express etc.)
    const iconClass = `creditcard-icon__${this.props.method.type}`;

    return (
        <li>
          <span className={iconClass}></span>
          <p className="details">Ending in {this.props.method.ending} expire {this.props.method.expires}</p>
          <p className="is-default">
          { this.props.method.isDefault &&
            '(default)'
          }
          { !this.props.method.isDefault &&
            <a
              href="#"
              onClick={this.handleSetDefault}
              className="setdefault__creditcard"
            >Set as Default</a>
          }
          </p>

          <span>
            <a href="#" className="remove__creditcard" onClick={this.openModal}></a>
            <ModalRemovePaymentMethod
              ref="removePaymentMethodModal"
              onConfirm={this.handleRemovePaymentMethod}
            />
          </span>
        </li>
    );
  },
});


export default DepositsPaymentsRow;
