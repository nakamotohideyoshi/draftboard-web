'use strict';

const React = require('react');

const ContestNavLineup = require('./contest-nav-lineup.jsx');
const ContestNavSeparator = require('./contest-nav-separator.jsx');


/**
 * Responsible for rendering the lineups list.
 */
const ContestNavLineupsList = React.createClass({

  propTypes: {
    lineups: React.PropTypes.array.isRequired
  },

  render() {
    const list = this.props.lineups.map((lineup) => {
      return [<ContestNavLineup key={lineup.id} lineup={lineup} />,
              <ContestNavSeparator key={lineup.id + 's'} half />];
    }).reduce((accum, l) => {
      // Just flatten the array on a single level. Not using lodash here,
      // because this may result in unexpected behavior depending on the
      // rendered React component internal representation.
      return accum.concat.apply(accum, l);
    }, []);

    return <div className="cmp-contest-nav--lineups-list">{list}</div>;
  }

});


module.exports = ContestNavLineupsList;
