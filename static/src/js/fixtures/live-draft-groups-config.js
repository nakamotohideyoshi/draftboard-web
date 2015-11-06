'use strict';


module.exports = [
  {
    pattern: '(.*)',

    fixtures: function(match, params, headers) {
      switch (match[1]) {
        case '/draft-group/1/':
          return require('./json/draft-group--1.json');
        // used to test that fantasy points do not exist
        case '/draft-group/114128/':
          return require('./json/draft-group--1.json');
        case '/draft-group/fantasy-points/1':
          return require('./json/draft-group--fantasy-points--1.json');
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
