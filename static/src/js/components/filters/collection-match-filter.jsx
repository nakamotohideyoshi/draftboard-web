import React from 'react';
import log from '../../lib/logging';
import find from 'lodash/find';
import isEqual from 'lodash/isEqual';


/**
 * Creates a radio-like selection list that filters the ContestStore.
 * Filtering actions are passed to the ContestStore via ContestActions.
 */
const CollectionMatchFilter = React.createClass({

  propTypes: {
    filters: React.PropTypes.array,
    // A default match to look for.
    match: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.array,
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
    elementType: React.PropTypes.string,
    activeFilter: React.PropTypes.object,
  },


  getDefaultProps() {
    return {
      activeFilter: {},
    };
  },


  getOptionsContainer() {
    let options = this.getOptions();

    if (this.props.elementType === 'select') {
      return (
        <div className="select-wrap">
          <select onChange={this.selectFilter}>{options}</select>
        </div>
      );
    }

    options = this.getSpans();
    return (
      <div>{options}</div>
    );
  },


  getOptions() {
    // Build up html for filter options.
    return this.props.filters.map((filter) => {
      let cssClass = 'cmp-collection-match-filter__option';

      // Add active class if the filter is currently active.
      if (
        this.props.activeFilter === '' && filter.match === '' ||
        isEqual(this.props.activeFilter.match, filter.match)
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
    });
  },


  getSpans() {
    const self = this;
    // Build up html for filter options.
    return this.props.filters.map((filter) => {
      let cssClass = 'cmp-collection-match-filter__option';

      // Add active class if the filter is currently active.
      if (
        this.props.activeFilter === '' && filter.match === '' ||
        isEqual(this.props.activeFilter.match, filter.match)
      ) {
        cssClass += ' cmp-collection-match-filter__option--active';
      }

      return (
        <span
          key={filter.match}
          className={cssClass}
          onClick={self.selectFilter.bind(self, filter)}
        >
          {filter.title}
        </span>
      );
    });
  },


  /**
   * Determines whether a row should be shown or not based on the selected filter criteria.
   * This works for either strings or an array of strings to match for.
   *
   * @param {Object} row - A row in the table.
   * @return {boolean} Should the row be displayed?
   */
  filter(row) {
    // First check that the row even contains the property we're trying to match against.
    if (!row.hasOwnProperty(this.props.filterProperty)) {
      log.warn('CollectionMatchFilter.filter() Row does not contain property',
          this.props.filterProperty
        );
      return true;
    }


    // Check if the row's property matches this filter's match value.
    switch (typeof this.props.activeFilter.match) {
      // If the match is a string...
      case 'string':
        if (this.state.match === '' ||
          row[this.props.filterProperty].toLowerCase() === this.props.activeFilter.match.toLowerCase()) {
          return true;
        }
        break;

      // But the match can also be an array. Like in MLB, 'OF' can be either 'lf','cf' or 'rf'.
      case 'object':
        if (
          this.props.activeFilter.match === '' ||
          this.props.activeFilter.match.indexOf(row[this.props.filterProperty].toLowerCase() !== -1)
        ) {
          return true;
        }
        break;

      default:
        return false;
    }

    // if a match was not found, return false.
    return false;
  },


  /**
   * When a user clicks on a filter, update this component and re-render the table.
   *
   * @param {Object} filter - The selected filter.
   * @param {string} filter.match
   */
  selectFilter(filter) {
    let activeFilter = filter;
    // We have to account for a select value being changed.
    if (filter.hasOwnProperty('target')) {
      // Find the filter with the title of the select value.
      activeFilter = find(this.props.filters, { title: filter.target.value });
    }

    // Update the filter match value in the app store. this will re-render the component
    // with the selected filter.
    this.props.onUpdate(this.props.filterName, this.props.filterProperty, activeFilter.match);
  },


  // Render filter options.
  render() {
    const filterClass = `${this.props.className} cmp-collection-match-filter`;
    const optionsContainer = this.getOptionsContainer();

    return (
      <div className={filterClass}>
        {optionsContainer}
      </div>
    );
  },

});

module.exports = CollectionMatchFilter;
