'use strict';

import React from 'react';


/**
 * Responsible for rendering the nav-scoreboard separator slash.
 */
const NavScoreboardSeparator = React.createClass({

  propTypes: {
    // Half or full sized slash?
    half: React.PropTypes.bool
  },

  shouldComponentUpdate() {
    return false;
  },

  render() {
    if (this.props.half) {
      return <div className="cmp-nav-scoreboard--separator half"></div>;
    } else {
      return <div className="cmp-nav-scoreboard--separator"></div>;
    }
  }

});


export default NavScoreboardSeparator;
