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
        <li key={entrant.username}>
          <span className="username">{entrant.username}</span>
        </li>
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
        <h6 className="header">
          <span className="prize">Entries</span>
        </h6>

        <ul>
          {this.getEntrantList(this.props.entrants)}
        </ul>
      </div>
    )
  }

})


module.exports = EntrantList
