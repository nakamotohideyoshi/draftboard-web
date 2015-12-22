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

    return (
      <div className="game scroll-item game--is-live">
        <div className="left">
          {game.homeTeamInfo.alias}
          <br />
          {game.awayTeamInfo.alias}
        </div>

        <div className="scores">
          {game.fields.home_score}
          <br />
          {game.fields.away_score}
        </div>

        <div className="right">
          {game.fields.clock}
          <br />
          {_.round(game.fields.quarter, 0)}
        </div>
      </div>
    )

  }

})


export default NavScoreboardGame
