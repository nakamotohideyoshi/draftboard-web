import React from 'react';
import NavScoreboardFilterItem from './nav-scoreboard-filter-item';


/*
 * Responsible for rendering the scoreboard navigation filters
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
    onChangeSelection: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    return {
      expanded: false,
      userSelectedOption: false,
    };
  },

  componentDidMount() {
    if (this.props.selected === null) {
      this.selectLargestOption();
    }
  },

  /**
   * If more sports loading in, then update to show the largest option
   */
  componentDidUpdate(prevProps) {
    if (this.props.options.length !== prevProps.options.length &&
        !this.state.userSelectedOption
    ) this.selectLargestOption();
  },

  /**
   * Selects largest available option.
   */
  selectLargestOption() {
    if (this.props.options.length === 0) {
      return;
    }

    const { option, type, key } = this.props.options.reduce((p, n) => (
      p.count > n.count ? p : n
    ));

    this.props.onChangeSelection(option, type, key);
  },

  /**
   * Show select menu options.
   */
  handleMenuShow() {
    this.setState({ expanded: true });
  },

  /**
   * Hide select menu options.
   */
  handleMenuLeave() {
    this.setState({ expanded: false });
  },

  /**
   * Change selected menu item.
   */
  handleChangeSelection(option) {
    const aside = document.querySelector('aside.sidebar');
    aside.classList.remove('sport-nfl');
    aside.classList.remove('sport-mlb');
    aside.classList.remove('sport-nhl');
    aside.classList.add(`sport-${sport}`);
    const results = this.props.options.filter((opt) => opt.option === option);
    const { type, key } = results[0];

    this.props.onChangeSelection(option, type, key);
    this.handleMenuLeave();
    this.setState({ userSelectedOption: true });
  },

  render() {
    const items = this.props.options.map((opt) => {
      const { option, count, key } = opt;

      return (
        <NavScoreboardFilterItem
          key={key}
          handleChangeSelection={this.handleChangeSelection}
          option={option}
          count={count}
        />
      );
    });

    return (
      <div className="cmp-nav-scoreboard--filters">
        <div className="cmp-nav-scoreboard--sport-nav select-list"
          onMouseEnter={this.handleMenuShow}
          onMouseLeave={this.handleMenuLeave}
        >
          <div className="select-list--selected">
            {this.props.selected}
            <svg
              className="icon icon-arrow down-arrow-icon"
              height="7"
              onClick={this.handleScrollRight}
              viewBox="0 0 16 16"
              width="7"
            >
              <g>
                <line strokeWidth="2.5" x1="10.3" y1="2.3" x2="4.5" y2="8.1" />
                <line strokeWidth="2.5" x1="3.6" y1="7.3" x2="10.1" y2="13.8" />
              </g>
            </svg>
          </div>
          <ul className={`select-list--options${(this.state.expanded ? ' visible' : '')}`}>
            <div className="arrow-up"></div>
            {items}
          </ul>
        </div>
      </div>
    );
  },
});


export default NavScoreboardFilters;
