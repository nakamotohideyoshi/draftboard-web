'use strict';

import React from 'react';

import NavScoreboardGame from './nav-scoreboard-game.jsx';
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx';


/**
 * Responsible for rendering the contest games list.
 */
const NavScoreboardGamesList = React.createClass({

  propTypes: {
    games: React.PropTypes.array.isRequired
  },

  render() {
    const list = this.props.games.map((game) => {
      return [<NavScoreboardGame key={game.id} game={game} />,
              <NavScoreboardSeparator key={game.id + 's'} half />];
    }).reduce((accum, l) => {
      // Just flatten the array on a single level. Not using lodash here,
      // because this may result in unexpected behavior depending on the
      // rendered React component internal representation.
      return accum.concat.apply(accum, l);
    }, []);

    return <div className="cmp-nav-scoreboard--games-list">{list}</div>;
  }

});


export default NavScoreboardGamesList;
