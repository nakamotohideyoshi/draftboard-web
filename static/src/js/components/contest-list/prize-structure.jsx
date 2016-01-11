import React from 'react'
import {forEach as _forEach} from 'lodash'
import {english as ordinal}  from  'ordinal'


var PrizeStructure = React.createClass({

  propTypes: {
    structure: React.PropTypes.object
  },


  getRanks: function() {
    let rankList = []

    if (typeof this.props.structure.info == 'undefined') {
      return ''
    }

     _forEach(this.props.structure.info.ranks, function(item) {
      rankList.push(
        <li key={item.rank}>
          <span className="place">{ordinal(item.rank)}</span>
          <span className="prize">${item.value}</span>
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
