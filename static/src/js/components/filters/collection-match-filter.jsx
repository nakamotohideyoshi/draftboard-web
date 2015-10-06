'use strict';

var React = require('react');
var log = require('../../lib/logging.js');


/**
 * Creates a radio-like selection list that filters the ContestStore.
 * Filtering actions are passed to the ContestStore via ContestActions.
 */
var CollectionMatchFilter = React.createClass({

  propTypes: {
    filters: React.PropTypes.array,
    // A default match to look for.
    match: React.PropTypes.string,
    // The propety in the row that we are filtering against.
    filterProperty: React.PropTypes.string.isRequired,
    className: React.PropTypes.string,
    // filterName is used in the datastore to store the active filter so other components can
    // reference it. Store.data.filters[{filterName}]
    filterName: React.PropTypes.string.isRequired,
    // When the filter values have changed, let the store it's registered with know so it can
    // re-run all of it's filters.
    onUpdate: React.PropTypes.func.isRequired,
    // Once the filter has mounted, it needs to register itself with a store.
    onMount: React.PropTypes.func.isRequired
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
        this.props.onUpdate(this.props.filterName, filter);
      });
  },


  componentDidMount: function() {
    // Register this filter with the Store with the provided function.
    this.props.onMount(this);
  },


  /**
   * Determines whether a row should be shown or not based on the selected filter criteria.
   *
   * @param {Object} row - A row in the table.
   * @return {boolean} Should the row be displayed?
   */
  filter: function(row) {

    if(!row.hasOwnProperty(this.props.filterProperty)) {
        log.warn('CollectionMatchFilter.filter() Row does not contain property',
          this.props.filterProperty);
        // return true;
    } else {
      // Check if the row's property matches this filter's match value.
      if (this.state.match === '' ||
          row[this.props.filterProperty].toLowerCase() === this.state.match.toLowerCase()) {
        return true;
      }

      return false;
    }

  },


  // Render filter options.
  render: function() {
    var filterClass = this.props.className + ' cmp-collection-match-filter';

    // Build up html for filter options.
    var filterOpts = this.props.filters.map(function(filter) {
      var cssClass = 'cmp-collection-match-filter__option';


      // Add active class if the filter is currently active.
      if(
        this.state.activeFilter === '' && filter.match === '' ||
        this.state.activeFilter.match === filter.match
      ) {
        cssClass += ' cmp-collection-match-filter__option--active';
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

module.exports = CollectionMatchFilter;
