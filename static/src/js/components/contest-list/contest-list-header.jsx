var React = require('react');
var renderComponent = require('../../lib/render-component');
// var ContestActions = require('../../actions/contest-actions.js');
const store = require('../../store');
const ReactRedux = require('react-redux');


/**
 * Render the header for a contest list - Displays currently active filters.
 */
var ContestListHeader = React.createClass({

  // mixins: [
  //   Reflux.connect(ContestStore)
  // ],

  propTypes: {
    contests: React.PropTypes.array.isRequired
  },


  revealFilters: function() {
    // ContestActions.contestTypeFiltered();
  },

  render: function() {
    // Determine the contest type filter title.
    var currentLeague;

    if (this.props.contests.activeFilters.hasOwnProperty('sportFilter')) {
      currentLeague = (
        <span>
          <span className="cmp-contest-list--sport">
            {this.props.contests.activeFilters.sportFilter.title} Contests
          </span>
          <span className="cmp-contest-list__header-divider">/</span>
        </span>
      );
    }

    if (!currentLeague || this.props.contests.activeFilters.sportFilter.title === 'All') {
      currentLeague = '';
    }

    // Determine the league filter title.
    var currentContestType;

    if (this.props.contests.activeFilters.hasOwnProperty('contestTypeFilter')) {
      currentContestType = this.props.contests.activeFilters.contestTypeFilter.title;
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


// =============================================================================
// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    contests: state.contests || []
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
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
