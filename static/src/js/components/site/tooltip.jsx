'use strict';

var React = require('react');


/**
 * A generic Tooltip component. You should wrap the contents of the tooltip in this component.
 * @param  {Boolean} isVisible: Set the initial visibility.
 * @param  {String}  position: top, bottom, left, right. - Check the css file for details.
 * @param  {String}  additionalClassName: Pass in any additional classNames you need for styling
 *                   purposes.
 */
var Tooltip = React.createClass({

  propTypes: {
    isVisible: React.PropTypes.bool,
    position: React.PropTypes.string,
    additionalClassName: React.PropTypes.string,
    children: React.PropTypes.element
  },


  getDefaultProps: function() {
    return {
      isVisible: true,
      position: 'bottom',
      additionalClassName: ''
    };
  },


  getInitialState: function() {
    return {
      isVisible: this.props.isVisible
    };
  },


  // Show the tooltip.
  show: function(callback) {
    callback = callback || function(){};
    this.setState({isVisible: true}, callback);
  },


  // Hide the tooltip.
  hide: function(callback) {
    callback = callback || function(){};
    this.setState({isVisible: false}, callback);
  },


  // Toggle the tooltip.
  toggle: function(callback) {
    callback = callback || function(){};
    var newVisibility = this.state.isVisible ? false : true;
    this.setState({isVisible: newVisibility}, callback);
  },


  /**
   * I'm pretty sure we'll always want to ignore a tooltip click... I think.
   */
  ignoreClick: function(e) {
    e.stopPropagation();
  },


  render: function() {
    // Add all the necessary css classes.
    var tipClass = "tooltip tooltip--" + this.props.position + "-arrow " +
        this.props.additionalClassName;

    if(!this.state.isVisible) {
      tipClass += " tooltip--hidden";
    }

    return (
      <div className={tipClass} onClick={this.ignoreClick}>
        <div className="tooltip__content">{this.props.children}</div>
      </div>
    );
  }

});


module.exports = Tooltip;
