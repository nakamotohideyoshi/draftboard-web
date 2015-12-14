'use strict';

import React from 'react';


/*
 *   Responsible for rendering the scoreboard navigation filters
 * select menu.
*/
const NavScoreboardFilters = React.createClass({

  propTypes: {
    // Selected option text.
    selected: React.PropTypes.any,

    // Options array:
    //
    //   option -> Option text
    //   type:  -> Option type
    //   key:   -> Option subtype
    //   count: -> Items count on this option
    //
    options: React.PropTypes.array.isRequired,

    //
    // Called on select menu change.
    //
    // @param {String} selectedOption Name of the selected option
    // @param {String} selectedType Type of the selected item
    // @param {String} selectedKey Key of the selected item type
    //
    onChangeSelection: React.PropTypes.func.isRequired
  },

  getInitialState() {
    return {expanded: false};
  },

  componentDidMount() {
    if (this.props.selected === null) {
      this.selectFirstOption();
    }
  },

  /**
   * Selects first available option.
  */
  selectFirstOption() {
    if (this.props.options.length === 0) {
      return
    }

    const {option, type, key} = this.props.options[0];

    this.props.onChangeSelection(option, type, key);
  },

  /**
   * Show select menu options.
  */
  handleMenuShow() {
    this.setState({expanded: true});
  },

  /**
   * Hide select menu options.
  */
  handleMenuLeave () {
    this.setState({expanded: false});
  },

  /**
   * Change selected menu item.
  */
  handleChangeSelection(option) {
    const results = this.props.options.filter((opt) => {
      return opt.option === option;
    });
    const {type, key} = results[0];

    this.props.onChangeSelection(option, type, key);
    this.handleMenuLeave();
  },

  render() {
    const items = this.props.options.map((opt) => {
      let {option, count} = opt;

      return (
        <li key={option} onClick={this.handleChangeSelection.bind(this, option)}>
          {option}
          <span className="counter"> {count}</span>
        </li>
      );
    });

    return (
      <div className="cmp-nav-scoreboard--filters">
        <div className="cmp-nav-scoreboard--sport-nav select-list"
             onMouseEnter={this.handleMenuShow}
             onMouseLeave={this.handleMenuLeave}>
          <div className="select-list--selected">{this.props.selected}</div>
          <ul className={"select-list--options" +
                         (this.state.expanded ? " visible" : "")}>
            <div className="arrow-up"></div>
            {items}
          </ul>
        </div>
      </div>
    );
  }

});


export default NavScoreboardFilters;
