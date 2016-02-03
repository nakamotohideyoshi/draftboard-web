import React from 'react';
import ReactDOM from 'react-dom';


/**
 * This simply renders the contents of a Modal compenent onto a div that is a child of the 'body'
 * tag with any classnames that are passed to it.
 */
const ModalWrap = React.createClass({

  propTypes: {
    children: React.PropTypes.element.isRequired,
    className: React.PropTypes.string,
  },


  componentDidMount() {
    const el = document.createElement('div');
    el.className = this.props.className;
    document.body.appendChild(el);
    this.modalElement = el;
    this.componentDidUpdate();
  },


  componentDidUpdate() {
    this.modalElement.className = this.props.className;
    ReactDOM.render(<div className="cmp-modal__inner">{this.props.children}</div>, this.modalElement);
  },


  componentWillUnmount() {
    document.body.removeChild(this.modalElement);
  },


  modalElement: null,


  render() {
    return null;
  },

});


module.exports = ModalWrap;
