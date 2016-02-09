import React from 'react';

import NavScoreboardGame from './nav-scoreboard-game.jsx';
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx';


/**
 * Responsible for rendering the contest games list.
 */
const NavScoreboardGamesList = React.createClass({

  propTypes: {
    sport: React.PropTypes.object.isRequired,
    games: React.PropTypes.object.isRequired,
  },

  // immutable = fast
  defaultList: [],

  render() {
    const list = this.props.sport.gameIds.map((gameId) => [
      <NavScoreboardGame key={gameId} game={this.props.games[gameId]} />,
      <NavScoreboardSeparator key={`${gameId}--separator'`} half />,

    // Just flatten the array on a single level. Not using lodash here,
    // because this may result in unexpected behavior depending on the
    // rendered React component internal representation.
    ]).reduce((accum, l) => accum.concat.apply(accum, l), this.defaultList);

    return <div className="cmp-nav-scoreboard--games-list">{list}</div>;
  },

});


export default NavScoreboardGamesList;
