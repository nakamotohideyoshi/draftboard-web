var React = require('react');
import log from '../../lib/logging';
var _find = require('lodash/collection/find');


/**
 * Creates a radio-like selection list that filters the ContestStore.
 * Filtering actions are passed to the ContestStore via ContestActions.
 */
var CollectionMatchFilter = React.createClass({

  propTypes: {
    filters: React.PropTypes.array,
    // A default match to look for.
    match: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.array
    ]),
    // The propety in the row that we are filtering against.
    filterProperty: React.PropTypes.string.isRequired,
    className: React.PropTypes.string,
    // filterName is used in the datastore to store the active filter so other components can
    // reference it. Store.data.filters[{filterName}]
    filterName: React.PropTypes.string.isRequired,
    // When the filter values have changed, let the store it's registered with know so it can
    // re-run all of it's filters.
    onUpdate: React.PropTypes.func.isRequired,
    // 'span' or 'select' - defaults to span.
    elementType: React.PropTypes.string
  },


  getInitialState: function() {
    return {
      // Initial match value.
      'match': this.props.match,
      // Used to update the rendered HTML with an active class.
      'activeFilter': {
        title: 'All'
      }
    };
  },


  /**
   * When a user clicks on a filter, update this component and re-render the table.
   *
   * @param {Object} filter - The selected filter.
   * @param {string} filter.match
   */
  selectFilter: function(filter) {
    // We have to account for a select value being changed.
    if (filter.hasOwnProperty('target')) {
      // Find the filter with the title of the select value.
      filter = _find(this.props.filters, 'title', filter.target.value);
    }

    // Update the filter match value, then tell the parent DataTable that the
    // filter has been updated - this will re-render() the DataTable.
    this.setState({
        'match': filter.match,
        'activeFilter': filter
      }, function() {
        this.props.onUpdate(this.props.filterName, this.props.filterProperty, filter.match);
      });
  },


  /**
   * Determines whether a row should be shown or not based on the selected filter criteria.
   * This works for either strings or an array of strings to match for.
   *
   * @param {Object} row - A row in the table.
   * @return {boolean} Should the row be displayed?
   */
  filter: function(row) {

    // First check that the row even contains the property we're trying to match against.
    if(!row.hasOwnProperty(this.props.filterProperty)) {
        log.warn('CollectionMatchFilter.filter() Row does not contain property',
          this.props.filterProperty
        );
        return true;
    }


    // Check if the row's property matches this filter's match value.
    switch (typeof this.state.match) {
      // If the match is a string...
      case 'string':
        if (this.state.match === '' ||
          row[this.props.filterProperty].toLowerCase() === this.state.match.toLowerCase()) {
          return true;
        }
        break;

      // But the match can also be an array. Like in MLB, 'OF' can be either 'lf','cf' or 'rf'.
      case 'object':
        if (this.state.match === '' ||
          -1 !== this.state.match.indexOf(row[this.props.filterProperty].toLowerCase())
        ) {
          return true;
        }
        break;
    }

    // if a match was not found, return false.
    return false;
  },


  getSpans: function() {
    // Build up html for filter options.
    return this.props.filters.map(function(filter) {
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
  },


  getOptions: function() {
    // Build up html for filter options.
    return this.props.filters.map(function(filter) {
      var cssClass = 'cmp-collection-match-filter__option';

      // Add active class if the filter is currently active.
      if(
        this.state.activeFilter === '' && filter.match === '' ||
        this.state.activeFilter.match === filter.match
      ) {
        cssClass += ' cmp-collection-match-filter__option--active';
      }

      return (
        <option
          key={filter.match}
          className={cssClass}
        >
          {filter.title}
        </option>
      );

    }.bind(this));
  },


  getOptionsContainer: function() {
    var options = this.getOptions();

    if (this.props.elementType == 'select') {
      return (
        <div className="select-wrap">
          <select onChange={this.selectFilter}>{options}</select>
        </div>
      );
    } else {
      options = this.getSpans();
      return (
        <div>{options}</div>
      );
    }
  },


  // Render filter options.
  render: function() {
    var filterClass = this.props.className + ' cmp-collection-match-filter';
    var optionsContainer = this.getOptionsContainer();

    return (
      <div className={filterClass}>
        {optionsContainer}
      </div>
    );
  }

});

module.exports = CollectionMatchFilter;
