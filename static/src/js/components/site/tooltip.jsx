import React from 'react';


/**
 * A generic Tooltip component. You should wrap the contents of the tooltip in this component.
 * @param  {Boolean} isVisible: Set the initial visibility.
 * @param  {String}  position: top, bottom, left, right. - Check the css file for details.
 * @param  {String}  additionalClassName: Pass in any additional classNames you need for styling
 *                   purposes.
 */
const Tooltip = React.createClass({

  propTypes: {
    // Default visiblity.
    isVisible: React.PropTypes.bool,
    position: React.PropTypes.string,
    additionalClassName: React.PropTypes.string,
    children: React.PropTypes.element,
    clickToClose: React.PropTypes.bool,
  },


  getDefaultProps() {
    return {
      isVisible: true,
      position: 'bottom',
      additionalClassName: '',
      clickToClose: false,
    };
  },


  getInitialState() {
    return {
      isVisible: this.props.isVisible,
    };
  },


  // We pass isVisible via props to set the default visiblity state. but we also want to be able
  // to override what the internal state is from a parent component, so if the props change, sync
  // up the state.
  componentWillReceiveProps(newProps) {
    this.setState({ isVisible: newProps.isVisible });
  },

  // Show the tooltip.
  show(callback = () => ({})) {
    this.setState({ isVisible: true }, callback);
  },


  // Hide the tooltip.
  hide(callback = () => ({})) {
    this.setState({ isVisible: false }, callback);
  },


  // Toggle the tooltip.
  toggle(callback = () => ({})) {
    const newVisibility = !this.state.isVisible;
    this.setState({ isVisible: newVisibility }, callback);
  },


  /**
   * Handle the tooltip click event.
   */
  handleClick(e) {
    // If we want it to close on click...
    if (this.props.clickToClose) {
      this.hide();
    } else {
      e.stopPropagation();
    }
  },


  render() {
    // Add all the necessary css classes.
    let tipClass = `tooltip tooltip--${this.props.position}-arrow ${this.props.additionalClassName}`;

    if (!this.state.isVisible) {
      tipClass += ' tooltip--hidden';
    }

    return (
      <div className={tipClass} onClick={this.handleClick}>
        <div className="tooltip__content">{this.props.children}</div>
      </div>
    );
  },
});


module.exports = Tooltip;
