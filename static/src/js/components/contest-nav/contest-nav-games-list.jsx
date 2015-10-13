'use strict';

const React = require('react');

const ContestNavGame = require('./contest-nav-game.jsx');
const ContestNavSeparator = require('./contest-nav-separator.jsx');


/**
 * Responsible for rendering the contest games list.
 */
const ContestNavGamesList = React.createClass({

  propTypes: {
    games: React.PropTypes.array.isRequired
  },

  render() {
    const list = this.props.games.map((game) => {
      return [<ContestNavGame key={game.id} game={game} />,
              <ContestNavSeparator key={game.id + 's'} half />];
    }).reduce((accum, l) => {
      // Just flatten the array on a single level. Not using lodash here,
      // because this may result in unexpected behavior depending on the
      // rendered React component internal representation.
      return accum.concat.apply(accum, l);
    }, []);

    return <div className="cmp-contest-nav--games-list">{list}</div>;
  }

});


module.exports = ContestNavGamesList;
