'use strict';

import React from 'react';
const Modal = require('../../modal/modal.jsx');


const ModalRemovePaymentMethod = React.createClass({

  propTypes: {
    onConfirm: React.PropTypes.func.isRequired
  },

  getInitialState() {
    return {isOpen: false};
  },

  open() {
    this.setState({isOpen: true});
  },

  close() {
    this.setState({isOpen: false});
  },

  render() {
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


export default ModalRemovePaymentMethod;
