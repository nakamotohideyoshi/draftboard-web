import React from 'react';
// import ModalAddPaymentMethod from './modal-add-payment-method.jsx';
import Modal from '../../modal/modal.jsx';
import CreditcardForm from '../../form-field/creditcard-form.jsx';


/**
 * Button / Link for adding new payment method connected with that user
 * Opens modal window in which form is provided, for inputting payment method options
 */
const DepositsAddPaymentMethod = React.createClass({

  getInitialState() {
    return {
      isOpen: false,
    };
  },


  openModal(event) {
    event.preventDefault();
    // this.refs.cardModal.open();
    this.setState({ isOpen: true });
  },

  // close modal
  close() {
    this.setState({ isOpen: false });
  },

  render() {
    return (
      <div className="form-field">

        <div className="form-field__content">
          <a
            href="#"
            className="add__paymentmethod"
            onClick={this.openModal}
          >
          + New payment method
          </a>

          <div>
            <Modal
              isOpen={this.state.isOpen}
              onClose={this.close}
              className="cmp-modal-payment-action"

            >
              <div>
                <div className="cmp-modal__content">
                  <CreditcardForm />
                  <div id="creditcard-form" />
                </div>
              </div>
            </Modal>
          </div>

        </div>
      </div>
    );
  },

});


module.exports = DepositsAddPaymentMethod;
