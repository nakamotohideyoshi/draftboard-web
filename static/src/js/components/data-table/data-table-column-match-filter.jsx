'use strict';

var React = require('react');
var renderComponent = require('../../lib/render-component');
var ContestActions = require('../../actions/contest-actions');


/**
 * Creates a radio-like selection list that filters a DataTable.
 * Filter actions are passed to a DataTable via DataTableActions.
 */
var DataTableColumnMatchFilter = React.createClass({

  propTypes: {
    filters: React.PropTypes.array,
    column: React.PropTypes.string,
    match: React.PropTypes.string,
    className: React.PropTypes.string
  },


  getInitialState: function() {
    return {
      // The table column to match against.
      'column': this.props.column,
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
        'activeFilter': filter.match
      }, function() {
        ContestActions.filterUpdated('DataTableColumnMatchFilter');
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
    // Check if the row's column matches this filter's match value.
    if (this.state.match === '' || row[this.state.column] === this.state.match) {
      return true;
    }

    return false;
  },


  // Render filter options.
  render: function() {
    var filterClass = this.props.className + ' data-table-filter';

    // Build up html for filter options.
    var filterOpts = this.props.filters.map(function(filter) {
      var cssClass = 'data-table-filter__option';

      // Add active class if the filter is currently active.
      if(this.state.activeFilter === filter.match) {
        cssClass += ' data-table-filter__option--active';
      }

      return (
        <span key={filter.match} className={cssClass} onClick={this.selectFilter.bind(this, filter)}>
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


renderComponent(<DataTableColumnMatchFilter />, '.table-contests-filter');

module.exports = DataTableColumnMatchFilter;
