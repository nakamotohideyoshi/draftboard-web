import React from 'react';
import * as AppActions from '../../stores/app-state-store.js';
import Sparkline from './sparkline.jsx';
import { find as _find } from 'lodash';


/**
 * Render a single Player 'row'.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
const DraftPlayerListRow = React.createClass({

  propTypes: {
    row: React.PropTypes.object.isRequired,
    focusPlayer: React.PropTypes.func,
    draftable: React.PropTypes.bool,
    drafted: React.PropTypes.bool,
    draftPlayer: React.PropTypes.func,
    unDraftPlayer: React.PropTypes.func,
  },


  getDefaultProps() {
    return {
      draftable: true,
    };
  },


  getInitialState() {
    return {};
  },


  onRowClick(playerId) {
    AppActions.openPane();
    this.props.focusPlayer(playerId);
  },


  onDraftClick(player, e) {
    e.stopPropagation();
    this.props.draftPlayer(player);
  },


  onUnDraftClick(player, e) {
    e.stopPropagation();
    this.props.unDraftPlayer(player.player_id);
  },


  getDraftButton() {
    if (this.props.drafted) {
      return (
        <div
          className="draft-button remove"
          onClick={this.onUnDraftClick.bind(this, this.props.row)}
        >Remove</div>
      );
    }

    return (
      <div
        className="draft-button"
        onClick={this.onDraftClick.bind(this, this.props.row)}
      >Draft</div>
    );
  },


  // Get the next game readout column: CLE @ SAS
  getNextGame() {
    if (this.props.row.nextGame && this.props.row.nextGame.homeTeam) {
      // get the home + away teams
      const homeTeam = _find(this.props.row.nextGame, { srid: this.props.row.nextGame.srid_home });
      const awayTeam = _find(this.props.row.nextGame, { srid: this.props.row.nextGame.srid_away });

      // if this player is on the away team, make that bold.
      if (this.props.row.team_srid === this.props.row.nextGame.srid_away) {
        return (
          <span><span className="player-team">{awayTeam.alias}</span> @ {homeTeam.alias}</span>
        );
      }
      // Otherwise, they are on the home team, make that bold.
      return (
        <span>{awayTeam.alias} @ <span className="player-team">{homeTeam.alias}</span></span>
      );
    }

    return (
      <span></span>
    );
  },

  render() {
    let classes = 'cmp-player-list__row';

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
        <td className="photo"><img src="/static/src/img/temp/PAM_90212.png" width="auto" height="35px" /></td>
        <td className="name">
          <span className="player">{this.props.row.name} </span>
          <span className="team">{this.props.row.team_alias}</span>
        </td>
        <td className="status">{this.props.row.status}</td>
        <td className="game">{this.getNextGame()}</td>
        <td>{this.props.row.fppg.toFixed(1)}</td>
        <td className="history"><Sparkline points={this.props.row.history} /></td>
        <td className="salary">${this.props.row.salary.toLocaleString('en')}</td>
      </tr>
    );
  },

});


module.exports = DraftPlayerListRow;
