'use strict'

import React from 'react'
import PureRenderMixin from 'react-addons-pure-render-mixin'

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
    const {home_abbr, away_abbr} = this.props.game.fields

    return (
      <div className="game scroll-item">
        <div className="left">
          {home_abbr}
          <br />
          {away_abbr}
        </div>

        <div className="right">
          7:10PM <br /> <br />
        </div>
      </div>
    )
  }

})


export default NavScoreboardGame
