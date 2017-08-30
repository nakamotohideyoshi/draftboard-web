import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Stats extends Component {
  getStatItems() {
    const statItems = [];
    for (let i = 0; i < this.props.player_stats.length; i++) {
      for (const key in this.props.player_stats[i]) {
        if (this.props.player_stats[i].hasOwnProperty(key)) {
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
                  <dt>{item}</dt>
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
  render() {
    return (
      <div className="stats">
        {this.getStatItems()}
      </div>
    );
  }
}

Stats.propTypes = {
  children: PropTypes.element,
  player_stats: PropTypes.array,
};

export default Stats;

