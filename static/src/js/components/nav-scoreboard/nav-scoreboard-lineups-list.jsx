import React from 'react';
import { map as _map } from 'lodash';
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
    const lineupsList = _map(this.props.lineups, (lineup) => lineup);
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
