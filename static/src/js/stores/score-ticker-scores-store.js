"use strict";

var Reflux = require('reflux');


var ScoreTickerScores = Reflux.createStore({
  scores: [],

  init: function() {
    this.fetchScores();
  },

  fetchScores: function() {

    this.scores = [
      {'title': 'BOS vs LAC', 'score': '03:06:23'},
      {'title': 'NY vs DEN', 'score': '04:06:23'},
      {'title': 'BOS vs LAC', 'score': '03:06:23'},
      {'title': 'NY vs DEN', 'score': '04:06:23'},
      {'title': 'BOS vs LAC', 'score': '03:06:23'},
      {'title': 'NY vs DEN', 'score': '04:06:23'},
      {'title': 'BOS vs LAC', 'score': '03:06:23'},
      {'title': 'NY vs DEN', 'score': '04:06:23'}
    ];

    this.trigger(self.scores);
  },

  getInitialState: function() {
    return this.scores;
  },

  getAllScores: function() {
    return this.scores;
  }

});


module.exports = ScoreTickerScores;
