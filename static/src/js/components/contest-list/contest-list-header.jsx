import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import * as ReactRedux from 'react-redux';
import { updateFilter } from '../../actions/contest-pool-actions.js';
import CollectionMatchFilter from '../filters/collection-match-filter.jsx';
const { Provider, connect } = ReactRedux;

// Options for the skill level filter.
const skillLevelFilters = [
  { title: 'Rookie', column: 'skill_level', match: ['rookie', 'all'] },
  { title: 'Veteran', column: 'skill_level', match: ['veteran', 'all'] },
];


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    contests: state.contestPools.allContests,
    filters: state.contestPools.filters,
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
  };
}


/**
 * Render the header for a contest list - Displays currently active filters.
 */
const ContestListHeader = (props) => (
  <div className="cmp-contest-list__header">
    <h4 className="title">Choose a Skill Level</h4>
    <div className="cmp-skill-level-filter">
      <CollectionMatchFilter
        className="contest-list-filter--skill-level"
        filters={skillLevelFilters}
        filterName="skillLevelFilter"
        filterProperty="skill_level.name"
        match={props.filters.skillLevelFilter.match}
        onUpdate={props.updateFilter}
        activeFilter={props.filters.skillLevelFilter}
      />
    </div>

    <div className="icon-key">
      <a href="#" className="fairmatch button button--outline">
        How Draftboard Works
      </a>
    </div>
  </div>
);


// Set the components propType validation.
ContestListHeader.propTypes = {
  contests: React.PropTypes.object,
  filters: React.PropTypes.object,
  updateFilter: React.PropTypes.func,
};


// Wrap the component to inject dispatch and selected state into it.
const ContestListHeaderConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(ContestListHeader);

renderComponent(
  <Provider store={store}>
    <ContestListHeaderConnected />
  </Provider>,
  '.cmp-contest-list-header'
);


module.exports = ContestListHeader;
