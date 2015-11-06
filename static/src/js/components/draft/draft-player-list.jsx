const React = require('react');
const ReactRedux = require('react-redux');
const store = require('../../store');
const renderComponent = require('../../lib/render-component');
// const CollectionMatchFilter = require('../filters/collection-match-filter.jsx');
// const CollectionSearchFilter = require('../filters/collection-search-filter.jsx');
const PlayerListRow = require('./draft-player-list-row.jsx');
import {fetchDraftGroup} from '../../actions/draft-group-actions.js';
// Other components that will take care of themselves on the draft page.
require('../contest-list/contest-list-header.jsx');
// require('../contest-list/contest-list-detail.jsx');
// require('../contest-list/contest-list-sport-filter.jsx');
// require('./draft-player-detail.jsx');


/**
 * Render a list of players able to be drafted.
 */
const DraftPlayerList = React.createClass({


  propTypes: {
    fetchDraftGroup: React.PropTypes.func.isRequired,
    allPlayers: React.PropTypes.array,
    filteredPlayers: React.PropTypes.array
  },


  // Contest type filter data.
  playerPositionFilters: [
    {title: 'All', column: 'position', match: ''},
    {title: 'PG', column: 'position', match: 'pg'},
    {title: 'SG', column: 'position', match: 'sg'},
    {title: 'SF', column: 'position', match: 'sf'},
    {title: 'PF', column: 'position', match: 'pf'},
    {title: 'C', column: 'position', match: 'c'}
  ],


  loadData: function() {
    // TODO: this sucks fix this.
    let draftgroupId = window.location.pathname.split('/')[2];

    this.props.fetchDraftGroup(draftgroupId);
  },


  getInitialState: function() {
    return ({
      filteredPlayers: [],
      newLineup: {
        availablePositions: []
      }
    });
  },


  getDefaultProps: function() {
    return {
      allPlayers: []
    };
  },


  //TODO: Make keyboard keys select players in the list.
  componentWillMount: function() {
    // Listen to j/k keypress actions to focus players.
    // KeypressActions.keypressJ.listen(this.focusNextRow);
    // KeypressActions.keypressK.listen(this.focusPreviousRow);
    this.loadData();
  },

  sortList: function(property) {
    console.log("sortList()", property);
    // DraftActions.setSortProperty(property);
  },


  render: function() {
    // Build up a list of rows to be displayed.
    var visibleRows = this.props.filteredPlayers.map(function(row) {
      var draftable = true;
      // Is there a slot available?
      if (this.state.newLineup.availablePositions.indexOf(row.position) === -1) {
        draftable = false;
      }
      // Can we afford this player?
      if (this.state.newLineup.remainingSalary < row.salary) {
        draftable = false;
      }

      return (
        <PlayerListRow
          key={row.player_id}
          row={row}
          draftable={draftable}
        />
      );
    }, this);

    // If the draftgroup hasn't been fetched yet, show a loading indicator.
    if(!this.props.allPlayers.length) {
      visibleRows = <tr><td colSpan="7"><h4>Loading Players.</h4></td></tr>;
    }

      // <div className="player-list-filter-set">
      //   <CollectionSearchFilter
      //     className="collection-filter--player-name"
      //     filterName="playerSearchFilter"
      //     filterProperty='player.name'
      //     match=''
      //     onUpdate={draftGroupActions.filterUpdated}
      //     onMount={draftGroupActions.registerFilter}
      //   />
      //
      // <CollectionMatchFilter
      //     className="collection-filter--player-type"
      //     filters={this.playerPositionFilters}
      //     filterName="contestTypeFilter"
      //     filterProperty='position'
      //     match=''
      //     onUpdate={draftGroupActions.filterUpdated}
      //     onMount={draftGroupActions.registerFilter}
      //   />
      // </div>

    return (
      <div>

        <table className="cmp-player-list__table table">
          <thead>
            <tr className="cmp-player-list__header-row">
              <th>POS</th>
              <th></th>
              <th
                className="table__sortable"
                onClick={this.sortList.bind(this, 'name')}>Player</th>
              <th>Status</th>
              <th>OPP</th>
              <th>FPPG</th>
              <th
                className="table__sortable"
                onClick={this.sortList.bind(this, 'salary')}>Salary</th>
              <th></th>
            </tr>
          </thead>
          <tbody>{visibleRows}</tbody>
        </table>
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
    allPlayers: state.draftDraftGroup.allPlayers || [],
    filteredPlayers: state.draftDraftGroup.allPlayers || [],
    sport: state.draftDraftGroup.sport
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchDraftGroup: (draftGroupId) => dispatch(fetchDraftGroup(draftGroupId))
  };
}

// Wrap the component to inject dispatch and selected state into it.
var DraftPlayerListConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftPlayerList);


renderComponent(
  <Provider store={store}>
    <DraftPlayerListConnected />
  </Provider>,
  '.cmp-player-list'
);



module.exports = DraftPlayerList;
