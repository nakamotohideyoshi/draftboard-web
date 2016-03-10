import React from 'react';
import renderComponent from '../../../lib/render-component';
import Modal from '../../modal/modal.jsx';
import CreditcardForm from '../../form-field/creditcard-form.jsx';


/**
 * Modal window, that has to render the CredicardForm in it
 * responsible for providing the user with the form needed to create new payment method
 */
const ModalAddPaymentMethod = React.createClass({

  getInitialState() {
    return { isOpen: false };
  },

  /**
   * When this component is mounted (the modal window inserted in the DOM)
   * find DOM element with ID `creditcard-form` and render <CreditcardForm /> component inplace
   */
  componentDidMount() {
    renderComponent(<CreditcardForm />, '#creditcard-form');
  },

  // open modal
  open() {
    this.setState({ isOpen: true });
  },

  // close modal
  close() {
    this.setState({ isOpen: false });
  },

  render() {
    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className="cmp-modal-payment-action"
      >
        <div>
          <div className="cmp-modal__content">
            <div id="creditcard-form" />
          </div>
        </div>
      </Modal>
    );
  },

});


module.exports = ModalAddPaymentMethod;
