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

    _forEach(entrants, (entrant, key) => {
      // Add the key index in case of username collisions on the react key prop.
      // without this we cannot render the same username twice.
      entrantList.push(
        <tr key={`${entrant.username}--${key}`}>
          <td className="username">{entrant.username}</td>
        </tr>
      );
    });

    return entrantList;
  },


  render() {
    if (!this.props.entrants) {
      return (
        <div></div>
      );
    }

    return (
      <div className="cmp-entrant-list">
        <table className="table">
          <thead>
            <tr>
              <th className="place">User</th>
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
