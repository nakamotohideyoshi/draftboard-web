'use strict'

import React from 'react'
import _ from 'lodash'

import NavScoreboardGame from './nav-scoreboard-game.jsx'
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx'


/**
 * Responsible for rendering the contest games list.
 */
const NavScoreboardGamesList = React.createClass({

  propTypes: {
    draftGroup: React.PropTypes.object.isRequired
  },

  render() {
    const boxScores = _.values(this.props.draftGroup.boxScores)

    const list = boxScores.map((game) => {
      return [<NavScoreboardGame key={game.srid} game={game} />,
              <NavScoreboardSeparator key={game.srid + 's'} half />]
    }).reduce((accum, l) => {
      // Just flatten the array on a single level. Not using lodash here,
      // because this may result in unexpected behavior depending on the
      // rendered React component internal representation.
      return accum.concat.apply(accum, l)
    }, [])

    return <div className="cmp-nav-scoreboard--games-list">{list}</div>
  }

})


export default NavScoreboardGamesList
