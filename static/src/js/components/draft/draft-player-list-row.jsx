'use strict';

var React = require('react');
var DraftActions = require("../../actions/draft-actions");
var AppActions = require("../../actions/app-actions");
var log = require('../../lib/logging.js');


/**
 * Render a single Player 'row'.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
var DraftPlayerListRow = React.createClass({

  propTypes: {
    row: React.PropTypes.object.isRequired,
    handleOnClick: React.PropTypes.func,
    draftable: React.PropTypes.bool
  },


  getInitialState: function() {
    return {};
  },


  getDefaultProps: function() {
    return {
      draftable: true
    };
  },


  onRowClick: function(playerId) {
    AppActions.openPane();
    log.debug('ContestListRow.onRowClick()', playerId);
    DraftActions.playerFocused(playerId);
  },


  onDraftClick: function(playerId, e) {
    log.debug('ContestListRow.onDraftClick()', playerId);
    e.stopPropagation();
    DraftActions.addPlayerToLineup(playerId);
  },


  render: function() {
    var classes = 'cmp-player-list__row';

    if (this.props.draftable === false) {
      classes += ' fade';
    }

    return (
      <tr
        key={this.props.row.player_id}
        className={classes}
        onClick={this.onRowClick.bind(this, this.props.row.player_id)}
      >
        <td>{this.props.row.position}</td>
        <td>{this.props.row.name} / {this.props.row.team_alias}</td>
        <td>STATUS</td>
        <td>OPP</td>
        <td>FPPG</td>
        <td>${this.props.row.salary.toLocaleString('en')}</td>
        <td>
          <div
            className="button--mini button--gradient"
            onClick={this.onDraftClick.bind(this, this.props.row.player_id)}
            >Draft</div>
        </td>
      </tr>
    );
  }

});


module.exports = DraftPlayerListRow;
