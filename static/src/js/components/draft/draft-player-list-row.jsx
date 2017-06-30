/* eslint no-param-reassign: 0 */
import React from 'react';
import * as AppActions from '../../stores/app-state-store';
import Sparkline from './sparkline';
import isEqual from 'lodash/isEqual';
import { focusPlayerSearchField, clearPlayerSearchField } from './draft-utils';
import DraftPlayerNextGame from './draft-player-next-game';


/**
 * Render a single Player 'row'.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
const DraftPlayerListRow = React.createClass({

  propTypes: {
    playerImagesBaseUrl: React.PropTypes.string.isRequired,
    row: React.PropTypes.object.isRequired,
    focusPlayer: React.PropTypes.func,
    draftPlayer: React.PropTypes.func,
    unDraftPlayer: React.PropTypes.func,
    isVisible: React.PropTypes.bool.isRequired,
    latestInjuryUpdate: React.PropTypes.object.isRequired,
  },


  shouldComponentUpdate(nextProps) {
    // shallowCompare does a poor job of actually discerning if the props have changed.
    // use a lodash deep-equal instead. Note: This comparison is slower, but leads to
    // significantly less re-renders.
    return !isEqual(this.props, nextProps);
  },


  onRowClick(playerId) {
    AppActions.openPane();
    this.props.focusPlayer(playerId);
  },


  onDraftClick(player, e) {
    e.stopPropagation();
    this.props.draftPlayer(player);
    clearPlayerSearchField();
    focusPlayerSearchField();
  },


  onUnDraftClick(player, e) {
    e.stopPropagation();
    this.props.unDraftPlayer(player.player_id);
    clearPlayerSearchField();
    focusPlayerSearchField();
  },


  getDraftButton() {
    if (this.props.row.drafted) {
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


  // Get any non-'active' status.
  getInjuryStatus(status) {
    if (status !== 'active') {
      return status;
    }

    return '';
  },


  render() {
    // console.log('render player');
    let classes = 'cmp-player-list__row';
    let salaryClasses = 'salary ';
    const statusClasses = this.props.row.status === 'active' ? 'positive status' : 'status';

    if (this.props.row.draftable === false) {
      classes += ' fade';
    }

    if (this.props.isVisible === false) {
      classes += ' hidden';
    }

    if (!this.props.row.canAfford) {
      salaryClasses += 'over-budget';
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
        <td className="photo">
          <img
            src={require('../../../img/blocks/draft-list/lineup-no-player.png')}
            data-src={`${this.props.playerImagesBaseUrl}/120/${this.props.row.player_srid}.png`}
            onError={(tag) => {
              tag.currentTarget.src = require('../../../img/blocks/draft-list/lineup-no-player.png');
            }}
            alt=""
            width="auto"
            height="35px"
          />
        </td>
        <td className="name">
          <span className="player">{this.props.row.name} </span>
          <span className="team">{this.props.row.teamCity} {this.props.row.teamName}</span>
        </td>
        <td className={statusClasses}>{this.props.row.status}</td>
        <td className="game">
          <DraftPlayerNextGame
            game={this.props.row.nextGame}
            highlightTeamSrid={this.props.row.team_srid}
          />
        </td>
        <td>{this.props.row.fppg.toFixed(1)}</td>
        <td className="history"><Sparkline points={this.props.row.history} /></td>
        <td className={salaryClasses}>${this.props.row.salary.toLocaleString('en')}</td>
      </tr>
    );
  },

});


module.exports = DraftPlayerListRow;
