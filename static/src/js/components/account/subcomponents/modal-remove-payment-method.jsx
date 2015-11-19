'use strict';

var React = require('react');
var Modal = require('../../modal/modal.jsx');

/**
 * Modal window (confirm window), that is to be used as a protection step from
 * iccidental removings of user's payment method
 */
var ModalRemovePaymentMethod = React.createClass({

  propTypes: {
    onConfirm: React.PropTypes.func.isRequired
  },

  getInitialState: function() {
    return {isOpen: false};
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
      >
        <div>
          <header className="cmp-modal__header">Are you sure you want to delete this credit card</header>

          <div className="cmp-modal__content">
            <form onSubmit={this.props.onConfirm} >
              <input
                type="submit"
                className="button--medium button--gradient--background button--gradient-outline button--confirm"
                value="Yes" />
            </form>
          </div>
        </div>
      </Modal>
    );
  }
});


module.exports = ModalRemovePaymentMethod;
