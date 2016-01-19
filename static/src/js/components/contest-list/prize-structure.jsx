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
        <tr key={item.rank}>
          <td className="place">{ordinal(item.rank)}</td>
          <td className="prize">${item.value}</td>
        </tr>
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
    )
  }

})


module.exports = PrizeStructure
