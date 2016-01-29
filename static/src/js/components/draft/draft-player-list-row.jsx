var React = require('react')
import * as AppActions from '../../stores/app-state-store.js'
import log from '../../lib/logging'
import Sparkline from './sparkline.jsx'


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
    drafted: React.PropTypes.bool,
    draftPlayer: React.PropTypes.func,
    unDraftPlayer: React.PropTypes.func
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


  onUnDraftClick: function(player, e) {
    e.stopPropagation()
    this.props.unDraftPlayer(player.player_id)
  },


  getDraftButton: function() {
    if (this.props.drafted) {
      return (
        <div
          className="draft-button remove"
          onClick={this.onUnDraftClick.bind(this, this.props.row)}
        >Remove</div>
      )
    } else {
      return (
        <div
          className="draft-button"
          onClick={this.onDraftClick.bind(this, this.props.row)}
        >Draft</div>
      )
    }
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
        <td className="draft">
          {this.getDraftButton()}
        </td>
        <td className="position">{this.props.row.position}</td>
        <td className="photo">👤</td>
        <td className="name">
          <span className="player">{this.props.row.name} </span>
          <span className="team">{this.props.row.team_alias}</span>
        </td>
        <td className="status">{this.props.row.status}</td>
        <td className="game"><span className="player-team">ME</span> @ YOU</td>
        <td>{this.props.row.fppg.toFixed(1)}</td>
        <td className="history"><Sparkline points={this.props.row.history} /></td>
        <td className="salary">${this.props.row.salary.toLocaleString('en')}</td>
      </tr>
    );
  }

})


module.exports = DraftPlayerListRow
