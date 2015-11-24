'use strict';

import React from 'react';

import NavScoreboardLineup from './nav-scoreboard-lineup.jsx';
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx';


/**
 * Responsible for rendering the lineups list.
 */
const NavScoreboardLineupsList = React.createClass({

  propTypes: {
    lineups: React.PropTypes.array.isRequired
  },

  render() {
    const list = this.props.lineups.map((lineup) => {
      return [<NavScoreboardLineup key={lineup.id} lineup={lineup} />,
              <NavScoreboardSeparator key={lineup.id + 's'} half />];
    }).reduce((accum, l) => {
      // Just flatten the array on a single level. Not using lodash here,
      // because this may result in unexpected behavior depending on the
      // rendered React component internal representation.
      return accum.concat.apply(accum, l);
    }, []);

    return <div className="cmp-nav-scoreboard--lineups-list">{list}</div>;
  }

});


export default NavScoreboardLineupsList;
