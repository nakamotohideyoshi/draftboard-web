'use strict';


module.exports = [
  {
    pattern: '(.*)',

    fixtures: function(match, params, headers) {
      switch (match[1]) {
        case '/prize/1':
          return require('./json/prize--1.json');
        case '/prize/114128/':
          throw new Error(404);
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
