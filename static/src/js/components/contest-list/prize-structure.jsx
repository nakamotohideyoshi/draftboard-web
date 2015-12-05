import React from 'react'
import {forEach as _forEach} from 'lodash'
import {english as ordinal}  from  'ordinal'


var PrizeStructure = React.createClass({

  propTypes: {
    structure: React.PropTypes.object
  },


  getRanks: function() {
    let place = 0
    let rankList = []

    if (typeof this.props.structure.info == 'undefined') {
      return ''
    }

     _forEach(this.props.structure.info.ranks, function(item) {
      place = place + 1
      rankList.push(
        <li key={place}>
          <span className="place">{ordinal(place)}</span>
          <span className="prize">${item.rank}</span>
        </li>
      )
    })

    return rankList
  },


  render: function() {

    if (!this.props.structure || this.props.structure.isFetching === true) {
      return (
        <div>Loading...</div>
      )
    }

    let rankList = this.getRanks()

    return (
      <div className="cmp-prize-structure">

        <h6 className="header">
          <span className="place">Position</span>
          <span className="prize">Prize</span>
        </h6>

        <ul>
          {rankList}
        </ul>
      </div>
    )
  }

})


module.exports = PrizeStructure
