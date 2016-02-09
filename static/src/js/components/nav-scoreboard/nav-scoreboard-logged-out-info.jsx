import React from 'react';


/**
 * Responsible for rendering the nav-scoreboard separator slash.
 */
const NavScoreboardLoggedOutInfo = React.createClass({

  shouldComponentUpdate() {
    return false;
  },

  render() {
    return (
      <div className="cmp-nav-scoreboard--logged-out-info">
        <a href="/login">Login</a>
        <a href="/register">Sign Up</a>
      </div>
    );
  },

});


export default NavScoreboardLoggedOutInfo;
