'use strict';

var React = require('react');
var renderComponent = require('../../lib/render-component');
var ContestActions = require('../../actions/contest-actions');


/**
 * Creates a radio-like selection list that filters the ContestStore.
 * Filtering actions are passed to the ContestStore via ContestActions.
 */
var ContestStorePropertyMatchFilter = React.createClass({

  propTypes: {
    filters: React.PropTypes.array,
    // A default match to look for.
    match: React.PropTypes.string,
    // The propety in the row that we are filtering against.
    property: React.PropTypes.string,
    className: React.PropTypes.string,
    // filterName is used in the ContestStore to store the active filter so other components can
    // reference it. ContestStore.data.filters[{filterName}]
    filterName: React.PropTypes.string
  },


  getDefaultProps: function() {
    return {
      'filterName': 'unnamed filter'
    };
  },


  getInitialState: function() {
    return {
      // Initial match value.
      'match': this.props.match,
      // Used to update the rendered HTML with an active class.
      'activeFilter': ''
    };
  },


  /**
   * When a user clicks on a filter, update this component and re-render the table.
   *
   * @param {Object} filter - The selected filter.
   * @param {string} filter.match
   */
  selectFilter: function(filter) {
    // Update the filter match value, then tell the parent DataTable that the
    // filter has been updated - this will re-render() the DataTable.
    this.setState({
        'match': filter.match,
        'activeFilter': filter
      }, function() {
        ContestActions.filterUpdated(this.props.filterName, filter);
      });
  },


  componentDidMount: function() {
    // Register the filter with the parent DataTable.
    ContestActions.registerFilter(this);
  },


  /**
   * Determines whether a row should be shown or not based on the selected filter criteria.
   *
   * @param {Object} row - A row in the table.
   * @return {boolean} Should the row be displayed?
   */
  filter: function(row) {
    // Check if the row's property matches this filter's match value.
    if (this.state.match === '' || row[this.props.property] === this.state.match) {
      return true;
    }

    return false;
  },


  // Render filter options.
  render: function() {
    var filterClass = this.props.className + ' contest-list-filter';

    // Build up html for filter options.
    var filterOpts = this.props.filters.map(function(filter) {
      var cssClass = 'contest-list-filter__option';


      // Add active class if the filter is currently active.
      if(
        this.state.activeFilter === '' && filter.match === '' ||
        this.state.activeFilter.match === filter.match
      ) {
        cssClass += ' contest-list-filter__option--active';
      }

      return (
        <span
          key={filter.match}
          className={cssClass}
          onClick={this.selectFilter.bind(this, filter)}
        >
          {filter.title}
        </span>
      );
    }.bind(this));

    return (
      <div className={filterClass}>
          {filterOpts}
      </div>
    );
  }

});


renderComponent(<ContestStorePropertyMatchFilter />, '.table-contests-filter');

module.exports = ContestStorePropertyMatchFilter;
