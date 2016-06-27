import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store.js';
import renderComponent from '../../lib/render-component';
import CollectionMatchFilter from '../filters/collection-match-filter.jsx';
import { updateFilter } from '../../actions/contest-pool-actions.js';
import { openDraftGroupSelectionModal } from '../../actions/upcoming-draft-groups-actions.js';
const { Provider, connect } = ReactRedux;
import filter from 'lodash/filter';
import find from 'lodash/find';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    sportFilter: state.contestPools.filters.sportFilter,
    contestPools: state.contestPools.allContests,
  };
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
    sportFilter: React.PropTypes.object,
    contestPools: React.PropTypes.object,
  },


  getInitialState() {
    return {
      // League filter data
      leagueFilters: [
        { title: 'MLB', column: 'sport', match: 'mlb' },
        { title: 'NBA', column: 'sport', match: 'nba' },
        { title: 'NFL', column: 'sport', match: 'nfl' },
        { title: 'NHL', column: 'sport', match: 'nhl' },
      ],
    };
  },

  /**
   * We only want to show filters that have active contest pools. This returns that.
   */
  getFiltersWithContestPools(leagueFilters, contestPools) {
    return filter(
      leagueFilters, (leagueFilter) => find(
        contestPools, (contestPool) => contestPool.sport === leagueFilter.match
      )
    );
  },


  handleFilterChange(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match);
  },


  render() {
    return (
      <div>
        <CollectionMatchFilter
          className="contest-list-filter--sport"
          filters={this.getFiltersWithContestPools(this.state.leagueFilters, this.props.contestPools)}
          filterProperty="sport"
          match=""
          filterName="sportFilter"
          onUpdate={this.handleFilterChange}
          activeFilter={this.props.sportFilter}
        />
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
