import React from 'react';
import { forEach as _forEach } from 'lodash';


/**
 * Renders a list of users entered into a contest
 */
const EntrantList = React.createClass({

  propTypes: {
    entrants: React.PropTypes.array,
  },


  getEntrantList(entrants) {
    const entrantList = [];

    _forEach(entrants, (entrant) => {
      entrantList.push(
        <tr key={entrant.username}>
          <td className="username">{entrant.username}</td>
        </tr>
      );
    });

    return entrantList;
  },


  render() {
    if (!this.props.entrants) {
      return (
        <div>Loading...</div>
      );
    }

    return (
      <div className="cmp-entrant-list">

        <table className="table">
          <thead>
            <tr>
              <th className="place">Entries</th>
            </tr>
          </thead>
          <tbody>
            {this.getEntrantList(this.props.entrants)}
          </tbody>
        </table>
      </div>
    );
  },

});


module.exports = EntrantList;
