'use strict';

var React = require('react');


/**
 * A search filter for a collection of  store data. Displays a compact search icon, when clicked
 * reveals a text input field that runs a string matching filter on the specified store data row
 * property.
 */
var CollectionSearchFilter = React.createClass({

  propTypes: {
    // The search value we are matching against - likely should be empty at first.
    match: React.PropTypes.string,
    // The propety in the row that we are filtering against.
    filterProperty: React.PropTypes.string.isRequired,
    // a classname to add to the component.
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


  getDefaultProps: function() {
    return {
      match: '',
      className: ''
    };
  },


  getInitialState: function() {
    return {
      // Initial match value.
      'match': this.props.match,
      // Default to compact state.
      'isExpanded': false
    };
  },


  /**
   * This filter performs a string match on the specified row property (this.props.filterProperty).
   * @param  {Object} row The single collection row.
   * @return {boolean} Should the row be displayed in the filtered collection list?
   */
  filter: function(row) {
    // Show the row if there is no search query.
    if (!this.state.match) {
      return true;
    }

    // We can account for nested resources here. so if we want to search for the row.player.name
    // property, just set 'row.player.name' as the search property, this will drill down into the
    // nested properties for it's search target.
    var nestedProps = this.props.filterProperty.split('.');
    var searchTarget = row;

    nestedProps.forEach(function(prop) {
      if (searchTarget.hasOwnProperty(prop)) {
        searchTarget = searchTarget[prop];
      }
    });

    // Search in the row's scpecified property for the search string.
    if (searchTarget.toLowerCase().indexOf(this.state.match.toLowerCase()) === -1) {
      return false;
    }
    // Default to show.
    return true;
  },


  componentDidMount: function() {
    // Register this filter with the Store with the provided function.
    this.props.onMount(this);
  },


  /**
   * When the searchField value changes, the Store will re-run any active filters via the provided
   * onUpdate function.
   * @param  {Object} e The dom event that triggered this.
   */
  handleChange: function(e) {
    this.setState({match: e.target.value}, function() {
      this.props.onUpdate(
        this.props.filterName,
        {title: this.props.filterName, column: this.props.filterProperty, match: this.state.match}
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
    var cmpClass = 'cmp-collection-search-filter ' + this.props.className;
    var openClass = this.state.isExpanded ? ' cmp-collection-search-filter--active ' : '';

    return (
      <div
        className={cmpClass + openClass}
        onClick={this.showSearchField}
      >
        <div className="cmp-collection-search-filter__sliding-door">
          <input
            ref="searchField"
            className="cmp-collection-search-filter__input"
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


module.exports = CollectionSearchFilter;
