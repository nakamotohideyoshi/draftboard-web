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
    game: React.PropTypes.object.isRequired
  },

  render() {
    const game = this.props.game
    let clockElement, scoresElement

    // if the game hasn't started
    if (!game.hasOwnProperty('boxscore')) {
      clockElement = (
        <div className="right">
          { moment(game.start).format('h:mma') } <br /> <br />
        </div>
      )
    } else {
      const boxScore = game.boxscore

      scoresElement = (
        <div className="scores">
          { boxScore.teamScores[game.srid_home] }
          <br />
          { boxScore.teamScores[game.srid_away] }
        </div>
      )


      // if the game has ended
      if (boxScore.status === 'closed') {
        clockElement = (
          <div className="right">
            Final
          </div>
        )

      // otherwise the game is live
      } else {
        let clock = boxScore.clock
        if (clock === '00:00') {
          clock = 'END OF'
        }

        clockElement = (
          <div className="right">
            { clock }
            <br />
            { boxScore.quarterDisplay }
          </div>
        )
      }
    }

    return (
      <div className="game scroll-item game--is-live">
        <div className="left">
          {game.homeTeamInfo.alias}
          <br />
          {game.awayTeamInfo.alias}
        </div>

        { scoresElement }
        { clockElement }
      </div>
    )
  }

})


export default NavScoreboardGame
