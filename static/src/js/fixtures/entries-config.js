'use strict';


module.exports = [
  {
    pattern: '(.*)',

    fixtures: function(match, params, headers) {
      switch (match[1]) {
        case '/contest/current-entries/':
          return require('./json/contest--current-entries.json');
      }
    },

    // `match`: result of the resolution of the regular expression
    // `data`: data returns by `fixtures` attribute
    callback: function (match, data) {
      return {
        body: data,
        text: data
      };
    }

  }
];
