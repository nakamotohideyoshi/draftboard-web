'use strict';

var React = require('react');
var ContestActions = require('../../actions/contest-actions');


/**
 * A search filter for the ContestStore. Displays a compact search icon, when clicked reveals
 * a text input field that runs a string matching filter on the specified contest row property.
 */
var ContestListSearchFilter = React.createClass({

  propTypes: {
    match: React.PropTypes.string,
    // The propety in the row that we are filtering against.
    property: React.PropTypes.string,
    className: React.PropTypes.string,
    // filterName is used in the ContestStore to store the active filter so other components can
    // reference it. ContestStore.data.filters[{filterName}]
    filterName: React.PropTypes.string
  },


  /**
   * This filter performs a string match on the specified row property (this.props.property).
   * @param  {Object} row The contest row.
   * @return {boolean} Should the row be displayed in the contest list?
   */
  filter: function(row) {
    // Show if there is no search query.
    if (!this.state.match) {
      return true;
    }
    // Search in the row's scpecified property for the search string.
    if (row[this.props.property].toLowerCase().indexOf(this.state.match.toLowerCase()) === -1) {
      return false;
    }
    // Default to show.
    return true;
  },


  getInitialState: function() {
    return {
      // Initial match value.
      'match': this.props.match,
      // Default to compact state.
      'isExpanded': false
    };
  },


  componentDidMount: function() {
    // Register this filter with the ContestStore.
    ContestActions.registerFilter(this);
  },


  /**
   * When the searchField value changes, the ContestStore will re-run any active filters and a new,
   * filtered set of contests will be passed into the ContestList.
   * @param  {Object} e The dom event that triggered this.
   */
  handleChange: function(e) {
    this.setState({match: e.target.value}, function() {
      ContestActions.filterUpdated(
        this.props.filterName,
        {title: this.props.filterName, column: this.props.property, match: this.state.match}
      );
    });
  },


  /**
   * Show the search field.
   */
  showSearchField: function() {
    this.setState({isExpanded: true});
    React.findDOMNode(this.refs.searchField).focus();
  },


  render: function() {
    var cmpClass = 'cmp-contest-list-search-filter contest-list-filter';
    var openClass = this.state.isExpanded ? ' cmp-contest-list-search-filter--active ' : '';

    return (
      <div
        className={cmpClass + openClass}
        onClick={this.showSearchField}
      >
        <div className="cmp-contest-list-search-filter__sliding-door">
          <input
            ref="searchField"
            className="cmp-contest-list-search-filter__input"
            type="text"
            value={this.state.match}
            onChange={this.handleChange}
            placeholder="Search"
          />
        </div>
      </div>
    );
  }

});


module.exports = ContestListSearchFilter;
