import React from 'react';
import ReactDom from 'react-dom';
import PubSub from 'pubsub-js';


/**
 * A search filter for a collection of  store data. Displays a compact search icon, when clicked
 * reveals a text input field that runs a string matching filter on the specified store data row
 * property.
 */
const CollectionSearchFilter = React.createClass({

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
  },


  getDefaultProps() {
    return {
      match: '',
      className: '',
    };
  },


  getInitialState() {
    return {
      // Initial match value.
      match: this.props.match,
      // Default to compact state.
      isExpanded: false,
    };
  },


  componentWillMount() {
    PubSub.subscribe('playerSearch.clear', () => {
      this.setState({
        match: '',
      }, () => {
        this.props.onUpdate(
          this.props.filterName,
          this.props.filterProperty,
          this.state.match
        );
      });
    });
  },


  /**
   * When the searchField value changes, the Store will re-run any active filters via the provided
   * onUpdate function.
   * @param  {Object} e The dom event that triggered this.
   */
  handleChange(e) {
    this.setState({ match: e.target.value }, () => {
      this.props.onUpdate(
        this.props.filterName,
        this.props.filterProperty,
        this.state.match
      );
    });
  },


  /**
   * Show the search field.
   */
  showSearchField() {
    this.setState({ isExpanded: true });
    ReactDom.findDOMNode(this.refs.searchField).focus();
  },


  render() {
    const cmpClass = `cmp-collection-search-filter ${this.props.className}`;
    const openClass = this.state.isExpanded ? ' cmp-collection-search-filter--active ' : '';

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
  },

});


module.exports = CollectionSearchFilter;
