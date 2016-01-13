import React from 'react'
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
var CollectionMatchFilter = require('../filters/collection-match-filter.jsx')
import {updateFilter} from '../../actions/upcoming-contests-actions.js'
import {openDraftGroupSelectionModal} from '../../actions/upcoming-draft-groups-actions.js'

/**
 * A league filter for a ContestList DataTable - This sits above the lineup cards in the sidebar.
 */
var ContestListSportFilter = React.createClass({

  propTypes: {
    updateFilter: React.PropTypes.func,
    openDraftGroupSelectionModal: React.PropTypes.func
  },


  getInitialState: function() {
    return {
      // League filter data - these will likely be replaced by dynamically determined values.
      leagueFilters: [
        {title: 'All', column: 'sport', match: ''},
        {title: 'NBA', column: 'sport', match: 'nba'},
        {title: 'NFL', column: 'sport', match: 'nfl'},
        {title: 'MLB', column: 'sport', match: 'mlb'}
      ]
    };
  },


  handleFilterChange: function(filterName, filterProperty, match) {
    this.props.updateFilter(filterName, filterProperty, match)
  },


  render: function() {
    return (
      <div>
        <CollectionMatchFilter
          className="contest-list-filter--sport"
          filters={this.state.leagueFilters}
          filterProperty='sport'
          match=''
          filterName='sportFilter'
          onUpdate={this.handleFilterChange}
          elementType='select'
        />
      <div
        className="add-lineup"
        onClick={this.props.openDraftGroupSelectionModal}
      >
          +
        </div>
      </div>
    );
  }

})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {};
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateFilter: (filterName, filterProperty, match) => dispatch(
      updateFilter(filterName, filterProperty, match)
    ),
    openDraftGroupSelectionModal: () => dispatch(openDraftGroupSelectionModal())
  }
}

// Wrap the component to inject dispatch and selected state into it.
var ContestListSportFilterConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(ContestListSportFilter)

// Render the component.
renderComponent(
  <Provider store={store}>
    <ContestListSportFilterConnected />
  </Provider>,
  '.cmp-contest-list-sport-filter'
);


module.exports = ContestListSportFilter
