import React from 'react';
import map from 'lodash/map';
import NavScoreboardLineup from './nav-scoreboard-lineup.jsx';
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx';


/**
 * Responsible for rendering the lineups list.
 */
const NavScoreboardLineupsList = React.createClass({

  propTypes: {
    lineups: React.PropTypes.object.isRequired,
  },

  defaultList: [],

  render() {
    const lineupsList = map(this.props.lineups, (lineup) => lineup);

    if (lineupsList.length === 0) {
      return <div className="cmp-nav-scoreboard--lineups-list" />;
    }

    const list = lineupsList.map((lineup) => [
      <NavScoreboardLineup key={lineup.id} lineup={lineup} />,
      <NavScoreboardSeparator key={`${lineup.id}s`} half />,

    // Just flatten the array on a single level. Not using lodash here,
    // because this may result in unexpected behavior depending on the
    // rendered React component internal representation.
    ]).reduce((accum, l) => accum.concat.apply(accum, l), this.defaultList);

    return <div className="cmp-nav-scoreboard--lineups-list">{list}</div>;
  },

});


export default NavScoreboardLineupsList;
