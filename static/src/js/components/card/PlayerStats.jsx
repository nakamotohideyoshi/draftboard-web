import React, { Component } from 'react';
import PropTypes from 'prop-types';
import log from '../../lib/logging';

// these static maps are completely because the api blows
// KR TD | PR TD | FR TD
const labelMap = {
  pass_yds: 'PASS YD',
  pass_td: 'PASS TD',
  ints: 'INT',
  rush_yds: 'RUSH YD',
  rush_td: 'RUSH TD',
  fum_rec: 'FUM',
  rec_rec: 'REC',
  rec_yds: 'REC YD',
  rec_td: 'REC TD',
  two_pt_conv: '2PC',
};
// needed to fill out the rows
const defaultPlayers = {
  QB: [
    'pass_yds',
    'pass_td',
    'ints',
    'rush_yds',
    'rush_td',
    'fum_rec',
  ],
  RB: [
    'rush_yds',
    'rush_td',
    'rec_rec',
    'rec_yds',
    'rec_td',
    'fum_rec',
  ],
  WR: [
    'rec_rec',
    'rec_yds',
    'rec_td',
    'rush_yds',
    'rush_td',
    'fum_rec',
  ],
  TE: [
    'rec_rec',
    'rec_yds',
    'rec_td',
    'rush_yds',
    'rush_td',
    'fum_rec',
  ],
  FX: [
    'rec_rec',
    'rec_yds',
    'rec_td',
    'rush_yds',
    'rush_td',
    'fum_rec',
  ],
};
class PlayerStats extends Component {
  getItemDefaultMarkup(pos) {
    return defaultPlayers[pos].map((entry) =>
      <dd className={`card-${entry}`}>
        <dl>
          <dt>{this.getLabel(entry, labelMap)}</dt>
          <dd>0</dd>
        </dl>
      </dd>
    );
  }
  getItemMarkup(stats, pos) {
    for (const key in stats) {
      if (stats.hasOwnProperty(key) && key !== 'children') {
        const tmparray = [];
        let item = this.getLabel(key, labelMap);
        let value = Math.floor(stats[key] * 100) / 100;
        log.info(key);
        // if the item exists in default and has no value show it
        if (defaultPlayers[pos].indexOf(key) >= 0 && stats[key] === 0) {
          tmparray.push([
            <dd key={item} className={`card-${item}`}>
              <dl>
                <dt>{item}</dt>
                <dd ref={key}>{value}</dd>
              </dl>
            </dd>,
          ]);
          // if the value is not 0 show it
        } else if (stats[key] !== 0) {
          tmparray.push([
            <dd key={item} className={`card-${item}`}>
              <dl>
                <dt>{item}</dt>
                <dd ref={key}>{value}</dd>
              </dl>
            </dd>,
          ]);
        }
        return tmparray;
      }
    }
  }
  // grabs the proper label for the stat from a map
  getLabel(item, lmap) {
    let label = '';
    for (const labelkey in lmap) {
      if (lmap.hasOwnProperty(labelkey) && item === labelkey) {
        label = lmap[labelkey];
      }
    }
    return label;
  }
  // build the actual markup for stats
  getStatItems() {
    const playerStats = this.buildPlayerStatArray(this.props.players);
    const position = this.props.players.roster_spot;
    let markup;
    if (this.props.players.player_stats !== undefined) {
      if (this.props.players.player_stats.length > 0) {
        markup = playerStats.map((playerstat) =>
          this.getItemMarkup(playerstat, position)
        );
      } else {
        // if the stats array is empty get the default
        markup = [this.getItemDefaultMarkup(position)];
      }
    } else {
      // not sure if I should have this here
      // it adds stats to the live panel
      markup = [this.getItemDefaultMarkup(position)];
    }
    return markup;
  }
  // helper for picking out values we don't want.
  playerStatsWhiteList(stat) {
    // this api is ridiculous
    // so much repeated values that already
    // exist in the parent
    // we need to seriously think about using graphQL
    const whitelist = [
      'pass_yds',
      'pass_td',
      'ints',
      'rush_yds',
      'rush_td',
      'fum_rec',
      'rec_rec',
      'rec_yds',
      'rec_td',
      'two_pt_conv',
    ];
    return whitelist.indexOf(stat) !== -1;
  }
  // perform some data cleanup before sending
  // it off to the markup render
  buildPlayerStatArray(player) {
    const stats = [];
    if (player.player_stats && player.player_stats.length) {
      for (const stat in player.player_stats[0]) {
        if (player.player_stats[0].hasOwnProperty(stat)) {
          // if not in blacklist push
          if (this.playerStatsWhiteList(stat)) {
            const statobj = {};
            statobj[stat] = player.player_stats[0][stat];
            stats.push(statobj);
          }
        }
      }
    }
    return stats;
  }

  render() {
    return (
      <div className="stats">
        <dl>{this.getStatItems()}</dl>
      </div>
    );
  }
}

PlayerStats.propTypes = {
  children: PropTypes.element,
  players: PropTypes.object,
};

export default PlayerStats;

