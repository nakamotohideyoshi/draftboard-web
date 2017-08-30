import React, { Component } from 'react';
import PropTypes from 'prop-types';
import log from '../../lib/logging';

class PlayerStats extends Component {
  getStatItems() {
    const statItems = [];
    log.info(this.props.player_stats);
    for (let i = 0; i < this.props.player_stats.length; i++) {
      for (const key in this.props.player_stats[i]) {
        if (this.props.player_stats[i].hasOwnProperty(key) && this.props.player_stats[i][key] > 0) {
          const item = key;
          let value = this.props.player_stats[i][key];
          // add $ sign if its needed
          if (
            item === 'remsalary' ||
            item === 'fees' ||
            item === 'playeravg') {
            value = `$${value}`;
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
  makeLabels(item) {
    const label = item.split('_').join(' ');
    return label;
  }
  render() {
    return (
      <div className="stats">
        {this.getStatItems()}
      </div>
    );
  }
}

PlayerStats.propTypes = {
  children: PropTypes.element,
  player_stats: PropTypes.array,
};

export default PlayerStats;

