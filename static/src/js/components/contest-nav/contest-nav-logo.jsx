'use strict';

const React = require('react');


/**
 * Responsible for rendering the contest-nav logo.
 */
const ContestNavLogo = React.createClass({

  shouldComponentUpdate() {
    return false;
  },

  render() {
    return (
      <div className="cmp-contest-nav--logo">
        <div className="logo"></div>
        <div className="text">Draftboard</div>
      </div>
    );
  }

});


module.exports = ContestNavLogo;
