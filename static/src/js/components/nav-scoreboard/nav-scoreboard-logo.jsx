import React from 'react';


/**
 * Responsible for rendering the nav-scoreboard logo.
 */
const NavScoreboardLogo = React.createClass({

  shouldComponentUpdate() {
    return false;
  },

  render() {
    return (
      <a href="/lobby/" className="cmp-nav-scoreboard--logo">
        <span className="logo"></span>
        <span className="text">Draftboard</span>
      </a>
    );
  },

});


export default NavScoreboardLogo;
