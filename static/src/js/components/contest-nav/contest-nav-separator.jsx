'use strict';

const React = require('react');


/**
 * Responsible for rendering the contest-nav separator slash.
 */
const ContestNavSeparator = React.createClass({

  propTypes: {
    // Half or full sized slash?
    half: React.PropTypes.bool
  },

  shouldComponentUpdate() {
    return false;
  },

  render() {
    if (this.props.half) {
      return <div className="cmp-contest-nav--separator half"></div>;
    } else {
      return <div className="cmp-contest-nav--separator"></div>;
    }
  }

});


module.exports = ContestNavSeparator;
