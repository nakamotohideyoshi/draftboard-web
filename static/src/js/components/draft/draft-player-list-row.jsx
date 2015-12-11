var React = require('react')
// var DraftActions = require("../../actions/draft-actions");
import * as AppActions from '../../stores/app-state-store.js'
var log = require('../../lib/logging.js')


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
    focusPlayer: React.PropTypes.func,
    draftable: React.PropTypes.bool,
    draftPlayer: React.PropTypes.func
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
    this.props.focusPlayer(playerId);
  },


  onDraftClick: function(player, e) {
    e.stopPropagation();
    this.props.draftPlayer(player);
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
        <td>👤</td>
        <td>{this.props.row.name} / {this.props.row.team_alias}</td>
        <td className="status">{this.props.row.status}</td>
        <td></td>
        <td>{this.props.row.fppg.toFixed(1)}</td>
        <td>${this.props.row.salary.toLocaleString('en')}</td>
        <td>
          <div
            className="button--mini button--gradient"
            onClick={this.onDraftClick.bind(this, this.props.row)}
            >Draft</div>
        </td>
      </tr>
    );
  }

})


module.exports = DraftPlayerListRow
