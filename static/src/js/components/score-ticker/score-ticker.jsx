"use strict";

var React = require('react');
var ScoreTickerStore = require('../../stores/score-ticker-scores-store');
var renderComponent = require('lib/render-component');

/**
 * The score ticker on the top of the page.
 */
var ScoreTicker = React.createClass({
  getInitialState: function() {
    return {scores: ScoreTickerStore.getAllScores()};
  },

  render: function() {
    var scoreItems = this.state.scores.map(function(score) {
      return <li className='component-score-ticker--score'>{score.title} - {score.score}</li>;
    });

    return (
      <ul className='component-score-ticker--scores'>
        {scoreItems}
      </ul>
    );
  }

});


// Render the component.
renderComponent(<ScoreTicker />, '.component-score-ticker');


module.exports = ScoreTicker;
