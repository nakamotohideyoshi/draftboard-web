import React from 'react';
import ModalWrap from './modal-wrap.jsx';
import classnames from 'classnames';
// import KeypressActions from '../../actions/keypress-actions';


/**
 * A component that creates a modal with a site-covering background element. Inspired by the Modal
 * component in Elemental UI (http://elemental-ui.com/modal).
 */
const Modal = React.createClass({

  propTypes: {
    // Should there be a button to close the modal?
    showCloseBtn: React.PropTypes.bool,
    children: React.PropTypes.element.isRequired,
    // Is the modal visible?
    isOpen: React.PropTypes.bool.isRequired,
    // Since the component can only handle user input and can't dicate whether it is visible or not
    // on it's own, we need this to pass a request from the user to close the modal back up to the
    // parent component.
    // This will be called when the user clicks the close button or the esc key or whatever else.
    // The function in the parent component needs to handle changing isOpen to false.
    onClose: React.PropTypes.func.isRequired,
    className: React.PropTypes.string,
  },


  getDefaultProps() {
    return {
      isOpen: false,
      showCloseBtn: true,
    };
  },


  handleClose() {
    this.props.onClose();
  },


  render() {
    const classNames = classnames(this.props.className, 'cmp-modal', { 'cmp-modal--visible': this.props.isOpen });
    let closeBtn = '';

    if (this.props.showCloseBtn) {
      closeBtn = (
      <div
        ref="closeBtn"
        className="cmp-modal__close"
        onClick={this.handleClose}
      />
      );
    }

    return (
      <ModalWrap className={classNames}>
        <div className="cmp-modal__dialog">
          {closeBtn}
          <div className="cmp-modal__content">
            {this.props.children}
          </div>

        </div>
      </ModalWrap>
    );
  },

});


module.exports = Modal;
