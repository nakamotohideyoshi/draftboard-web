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
      <a href="/" className="cmp-contest-nav--logo">
        <span className="logo"></span>
        <span className="text">Draftboard</span>
      </a>
    );
  }

});


module.exports = ContestNavLogo;
