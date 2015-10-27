'use strict';

var React = require('react');
var ReactDOM = require('react-dom');


/**
 * This simply renders the contents of a Modal compenent onto a div that is a child of the 'body'
 * tag with any classnames that are passed to it.
 */
var ModalWrap = React.createClass({

  propTypes: {
    children: React.PropTypes.element.isRequired,
    className: React.PropTypes.string
  },

  modalElement: null,

  componentDidMount: function() {
    var el = document.createElement('div');
    el.className = this.props.className;
    document.body.appendChild(el);
    this.modalElement = el;
    this.componentDidUpdate();
  },

  componentWillUnmount: function() {
    document.body.removeChild(this.modalElement);
  },

  componentDidUpdate: function() {
    this.modalElement.className = this.props.className;
    ReactDOM.render(<div className="cmp-modal__inner">{this.props.children}</div>, this.modalElement);
  },

  render: function() {
    return null;
  }

});


module.exports = ModalWrap;
