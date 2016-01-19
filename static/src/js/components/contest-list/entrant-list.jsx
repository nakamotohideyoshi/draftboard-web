import React from 'react'
import {forEach as _forEach} from 'lodash'


var EntrantList = React.createClass({

  propTypes: {
    entrants: React.PropTypes.array
  },


  getEntrantList: function(entrants) {
    let entrantList = []

    _forEach(entrants, function(entrant) {
      entrantList.push(
        <tr key={entrant.username}>
          <td className="username">{entrant.username}</td>
        </tr>
      )
    }.bind(this))

    return entrantList
  },


  render: function() {
    if (!this.props.entrants) {
      return (
        <div>Loading...</div>
      )
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
    )
  }

})


module.exports = EntrantList
