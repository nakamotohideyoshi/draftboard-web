import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Stats extends Component {
  getStatItems() {
    const statItems = [];

    for (const key in this.props) {
      if (this.props.hasOwnProperty(key)) {
        const item = key;
        let value = this.props[key];

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
};

export default Stats;

