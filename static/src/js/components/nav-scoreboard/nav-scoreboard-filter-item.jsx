import React from 'react';


/*
 * Dumb component for a filter item
*/
const NavScoreboardFilterItem = React.createClass({

  propTypes: {
    count: React.PropTypes.number,
    handleChangeSelection: React.PropTypes.func,
    option: React.PropTypes.string.isRequired,
  },

  // After the first render, we don't ever want to overwrite the noUiSlider DOM element. If we did,
  // we'd have to reinstantiate the slider.
  shouldComponentUpdate() {
    return false;
  },

  _onClick() {
    this.props.handleChangeSelection(this.props.option)
  },

  render() {
    return (
      <li onClick={this._onClick}>
        {this.props.option}
        <span className="counter"> {this.props.count}</span>
      </li>
    );
  },
});


export default NavScoreboardFilterItem;
