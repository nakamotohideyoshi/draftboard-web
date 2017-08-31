import React, { Component } from 'react';
import PropTypes from 'prop-types';
// import log from '../../lib/logging';

class PlayerStats extends Component {
  componentWillMount() {
    this.setState(
      {
        hasStats: false,
      }
    );
  }
  componentDidMount() {
    this.checkForStats();
  }

  getStatItems() {
    const statItems = [];
    const playerStats = this.buildPlayerStatArray(this.props.player_stats);

    for (let i = 0; i < playerStats.length; i++) {
      for (const key in playerStats[i]) {
        if (playerStats[i].hasOwnProperty(key) && playerStats[i][key] !== 0) {
          let item = key;
          let value = playerStats[i][key];
          if (item === 'fp_change') {
            item = 'fp_cng';
          }
          if (item === 'rush_yds') {
            item = 'rsh_yds';
          }
          if (item !== 'children') {
            statItems.push([
              <dd key={item} className={`card-${item}`}>
                <dl>
                  <dt>{this.makeLabels(item)}</dt>
                  <dd ref={key} >{value}</dd>
                </dl>
              </dd>,
            ]);
          }
        }
      }
    }
    return statItems;
  }

  checkForStats() {
    const arr = this.buildPlayerStatArray(this.props.player_stats);
    if (arr.length > 0) {
      this.setState({ hasStats: true });
    }
  }

  playerStatsBlackList(stat) {
    // this api is ridiculous
    // so much repeated values that already
    // exist in the parent
    // we need to seriously think about using graphQL
    const blacklist = [
      'created',
      'updated',
      'srid_game',
      'srid_player',
      'player_id',
      'player_type',
      'game_type',
      'game_id',
      'position',
      'fantasy_points',
    ];
    return blacklist.indexOf(stat) !== -1;
  }

  buildPlayerStatArray(player) {
    const stats = [];
    if (player.player_stats && player.player_stats.length) {
      for (const stat in player.player_stats[0]) {
        if (player.player_stats[0].hasOwnProperty(stat)) {
          // if not in blacklist push
          if (!this.playerStatsBlackList(stat)) {
            const statobj = {};
            statobj[stat] = player.player_stats[0][stat];
            stats.push(statobj);
          }
        }
      }
    }
    return stats;
  }

  makeLabels(item) {
    return item.split('_').join(' ');
  }

  render() {
    let hasStats = '';
    if (this.state.hasStats) {
      hasStats = 'has-stats';
    }
    return (
      <div className={`stats ${hasStats}`}>
        <dl>{this.getStatItems()}</dl>
      </div>
    );
  }
}

PlayerStats.propTypes = {
  children: PropTypes.element,
  player_stats: PropTypes.object,
};

export default PlayerStats;

