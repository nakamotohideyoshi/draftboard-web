import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store.js';
import renderComponent from '../../lib/render-component';
import CollectionMatchFilter from '../filters/collection-match-filter.jsx';
import { updateFilter } from '../../actions/upcoming-contests-actions.js';
import { openDraftGroupSelectionModal } from '../../actions/upcoming-draft-groups-actions.js';

const { Provider, connect } = ReactRedux;


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps() {
  return {};
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    updateFilter: (filterName, filterProperty, match) => dispatch(
      updateFilter(filterName, filterProperty, match)
    ),
    openDraftGroupSelectionModal: () => dispatch(openDraftGroupSelectionModal()),
  };
}


/**
 * A league filter for a ContestList DataTable - This sits above the lineup cards in the sidebar.
 */
const ContestListSportFilter = React.createClass({

  propTypes: {
    updateFilter: React.PropTypes.func.isRequired,
    openDraftGroupSelectionModal: React.PropTypes.func,
  },


  getInitialState() {
    return {
      // League filter data - these will likely be replaced by dynamically determined values.
      leagueFilters: [
        { title: 'All', column: 'sport', match: '' },
        { title: 'NBA', column: 'sport', match: 'nba' },
        { title: 'NFL', column: 'sport', match: 'nfl' },
        { title: 'NHL', column: 'sport', match: 'nhl' },
        { title: 'MLB', column: 'sport', match: 'mlb' },
      ],
    };
  },


  handleFilterChange(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match);
  },


  render() {
    return (
      <div>
        <CollectionMatchFilter
          className="contest-list-filter--sport"
          filters={this.state.leagueFilters}
          filterProperty="sport"
          match=""
          filterName="sportFilter"
          onUpdate={this.handleFilterChange}
          elementType="select"
        />
      <div
        className="add-lineup"
        onClick={this.props.openDraftGroupSelectionModal}
      >
          +
        </div>
      </div>
    );
  },

});


// Wrap the component to inject dispatch and selected state into it.
const ContestListSportFilterConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(ContestListSportFilter);

// Render the component.
renderComponent(
  <Provider store={store}>
    <ContestListSportFilterConnected />
  </Provider>,
  '.cmp-contest-list-sport-filter'
);


module.exports = ContestListSportFilter;
