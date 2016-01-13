'use strict'

import React from 'react'
import PureRenderMixin from 'react-addons-pure-render-mixin'
import _ from 'lodash'
import moment from 'moment'

/**
 * Responsible for rendering a singe contest game item.
 */
const NavScoreboardGame = React.createClass({

  mixins: [PureRenderMixin],

  propTypes: {
    // Example game:
    //
    // id':      '0'
    // time':    '7:10PM'
    // players': ['ATL', 'BAL']
    //
    game: React.PropTypes.object.isRequired
  },

  render() {
    const game = this.props.game
    const {home_abbr, away_abbr} = this.props.game.fields
    let clock

    let start = moment(game.fields.start)

    if (game.timeRemaining === null || moment().isBefore(start)) {
      return (
        <div className="game scroll-item">
          <div className="left">
            {this.props.game.homeTeamInfo.alias}
            <br />
            {this.props.game.awayTeamInfo.alias}
          </div>

          <div className="right">
            {moment(game.fields.start).format('h:mma')} <br /> <br />
          </div>
        </div>
      )
    }

    if (game.fields.status === 'closed') {
      clock = (
        <div className="right">
          Final
        </div>
      )
    } else {
      let quarter = _.round(game.fields.quarter, 0)
      if (quarter > 4 ) {
        quarter = (quarter % 4).toString() + 'OT'

        if (quarter === '1OT') {
          quarter = 'OT'
        }
      }

      clock = (
        <div className="right">
          { game.fields.clock }
          <br />
          { quarter }
        </div>
      )
    }

    return (
      <div className="game scroll-item game--is-live">
        <div className="left">
          {game.homeTeamInfo.alias}
          <br />
          {game.awayTeamInfo.alias}
        </div>

        <div className="scores">
          {game.teams[game.fields.srid_home].score}
          <br />
          {game.teams[game.fields.srid_away].score}
        </div>

        { clock }
      </div>
    )

  }

})


export default NavScoreboardGame
