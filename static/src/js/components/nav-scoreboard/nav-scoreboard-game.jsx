'use strict'

import React from 'react'
import PureRenderMixin from 'react-addons-pure-render-mixin'
import _ from 'lodash'

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

    if (game.timeRemaining === null) {
      return (
        <div className="game scroll-item">
          <div className="left">
            {this.props.game.homeTeamInfo.alias}
            <br />
            {this.props.game.awayTeamInfo.alias}
          </div>

          <div className="right">
            7:10PM <br /> <br />
          </div>
        </div>
      )
    }

    if (game.fields.clock === '00:00' && game.fields.quarter === '4.0') {
      clock = (
        <div className="right">
          Final
        </div>
      )
    } else {
      clock = (
        <div className="right">
          { game.fields.clock }
          <br />
          {_.round(game.fields.quarter, 0)}
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
