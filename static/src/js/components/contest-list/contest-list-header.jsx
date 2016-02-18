import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import ReactRedux from 'react-redux';
import * as AppActions from '../../stores/app-state-store.js';

const { Provider, connect } = ReactRedux;


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    contests: state.upcomingContests.allContests,
    filters: state.upcomingContests.filters,
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps() {
  return {};
}


/**
 * Render the header for a contest list - Displays currently active filters.
 */
const ContestListHeader = React.createClass({

  propTypes: {
    contests: React.PropTypes.object,
    filters: React.PropTypes.object,
  },


  toggleFilters() {
    AppActions.toggleContestFilters();
  },

  render() {
    // Determine the contest type filter title.
    let currentLeague;

    if (this.props.filters.hasOwnProperty('sportFilter')) {
      currentLeague = (
        <span>
          <span className="cmp-contest-list--sport">
            {this.props.filters.sportFilter.title} Contests
          </span>
          <span className="cmp-contest-list__header-divider">/</span>
        </span>
      );
    }

    if (!currentLeague || this.props.filters.sportFilter.title === 'All') {
      currentLeague = '';
    }

    // Determine the league filter title.
    let currentContestType;

    if (this.props.filters.sportFilter.hasOwnProperty('match')) {
      if (this.props.filters.sportFilter.match) {
        currentContestType = this.props.filters.sportFilter.match.toUpperCase();
      }
    }

    if (!currentContestType || currentContestType === 'All') {
      currentContestType = 'All Upcoming';
    }

    return (
      <div className="cmp-contest-list__header" onClick={this.toggleFilters}>
        <h2>
          {currentLeague}
          <span className="cmp-contest-list__header-type">{currentContestType}</span>
        </h2>
      </div>
    );
  },

});


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
