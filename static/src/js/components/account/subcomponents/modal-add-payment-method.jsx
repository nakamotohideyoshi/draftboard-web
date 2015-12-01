'use strict';

var React = require('react');
var renderComponent = require('../../../lib/render-component');
var Modal = require('../../modal/modal.jsx');
var CreditcardForm = require('../../form-field/creditcard-form.jsx');


/**
 * Modal window, that has to render the CredicardForm in it
 * responsible for providing the user with the form needed to create new payment method
 */
var ModalAddPaymentMethod = React.createClass({

  getInitialState: function() {
    return {isOpen: false};
  },

  /**
   * When this component is mounted (the modal window inserted in the DOM)
   * find DOM element with ID `creditcard-form` and render <CreditcardForm /> component inplace
   */
  componentDidMount: function() {
    renderComponent(<CreditcardForm />, '#creditcard-form');
  },

  // open modal
  open: function() {
    this.setState({isOpen: true});
  },

  // close modal
  close: function() {
    this.setState({isOpen: false});
  },

  render: function() {
    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className='cmp-modal-payment-action'
      >
        <div>
          <div className="cmp-modal__content">
            <div id="creditcard-form" />
          </div>
        </div>
      </Modal>
    );
  }

});

module.exports = ModalAddPaymentMethod;
