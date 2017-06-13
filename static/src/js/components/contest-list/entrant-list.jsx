import React from 'react';
import forEach from 'lodash/forEach';


/**
 * Renders a list of users entered into a contest
 */
const EntrantList = React.createClass({

  propTypes: {
    entrants: React.PropTypes.array,
    excludeUsernames: React.PropTypes.array,
  },


  getDefaultProps() {
    return {
      excludeUsernames: [],
    };
  },


  getEntrantList(entrants) {
    const entrantList = [];

    forEach(entrants, (entrant, key) => {
      // Add the key index in case of username collisions on the react key prop.
      // without this we cannot render the same username twice.
      if (this.props.excludeUsernames.indexOf(entrant.username) < 0) {
        entrantList.push(
          <tr key={`${entrant.username}--${key}`}>
            <td className="username">{entrant.username}</td>
          </tr>
        );
      }
    });

    return entrantList;
  },


  render() {
    if (!this.props.entrants) {
      return (
        <div className="cmp-entrant-list"></div>
      );
    }

    return (
      <div className="cmp-entrant-list">
        <table className="table">
          <tbody>
            {this.getEntrantList(this.props.entrants)}
          </tbody>
        </table>
      </div>
    );
  },

});


module.exports = EntrantList;
