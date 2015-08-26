'use strict';

var React = require('react');


/**
 * The [ 1x | Enter ] button on a contest list.
 */
var MultiEntryButton = React.createClass({

  /**
   * Ignore the click event of the button. Makes it so the contest details don't pop open when you
   * enter a contest.
   */
  ignoreClick: function(e) {
    e.stopPropagation();
  },


  render: function() {
    return (
      <span className="button-multi" onClick={this.ignoreClick}>
        <select>
          <option>1x</option>
          <option>2x</option>
          <option>3x</option>
          <option>4x</option>
          <option>5x</option>
          <option>6x</option>
          <option>7x</option>
          <option>8x</option>
          <option>9x</option>
          <option>10x</option>
        </select>
        <input type="submit" value="Enter" />
      </span>
    );
  }

});


module.exports = MultiEntryButton;
