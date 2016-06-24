import React from 'react';
import forEach from 'lodash/forEach';
import ordinal from '../../lib/ordinal.js';
import { humanizeCurrency } from '../../lib/utils/currency.js';


/**
 * Render a contest's prize structure.
 */
const PrizeStructure = React.createClass({

  propTypes: {
    structure: React.PropTypes.object,
  },


  getRanks() {
    const rankList = [];

    forEach(this.props.structure.ranks, (item) => {
      rankList.push(
        <tr key={item.rank}>
          <td className="place">{ordinal(item.rank)}</td>
          <td className="prize">{humanizeCurrency(item.value)}</td>
        </tr>
      );
    });

    return rankList;
  },


  render() {
    const rankList = this.getRanks();

    return (
      <div className="cmp-prize-structure">
        <table className="table">
          <thead>
            <tr>
              <th className="place">Position</th>
              <th className="prize">Prize</th>
            </tr>
          </thead>
          <tbody>
            {rankList}
          </tbody>
        </table>
      </div>
    );
  },

});


module.exports = PrizeStructure;
