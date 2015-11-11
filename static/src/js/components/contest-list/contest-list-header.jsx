var React = require('react')
var renderComponent = require('../../lib/render-component')
// var ContestActions = require('../../actions/contest-actions.js');
const store = require('../../store')
const ReactRedux = require('react-redux')
import * as AppActions from '../../stores/app-state-store.js'


/**
 * Render the header for a contest list - Displays currently active filters.
 */
var ContestListHeader = React.createClass({

  propTypes: {
    contests: React.PropTypes.object,
    filters: React.PropTypes.object
  },


  revealFilters: function() {
    AppActions.contestTypeFiltered();
  },

  render: function() {
    // Determine the contest type filter title.
    var currentLeague;

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
    var currentContestType;

    if (this.props.filters.sportFilter.hasOwnProperty('match')) {
      currentContestType = this.props.filters.sportFilter.match;
    }

    if (!currentContestType || currentContestType === 'All') {
      currentContestType = 'All Upcoming';
    }

    return (
      <div className="cmp-contest-list__header" onClick={this.revealFilters}>
        <h2>
          {currentLeague}
          <span className="cmp-contest-list__header-type">{currentContestType}</span>
        </h2>
      </div>
    );
  }

});


// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    contests: state.upcomingContests.allContests,
    filters: state.upcomingContests.filters
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps() {
  return {};
}

// Wrap the component to inject dispatch and selected state into it.
var ContestListHeaderConnected = connect(
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
