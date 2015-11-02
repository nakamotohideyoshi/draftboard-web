'use strict';

// custom txt require as string, solved by http://goo.gl/ZmalV3
var fs = require('fs');
require.extensions['.txt'] = function (module, filename) {
    module.exports = fs.readFileSync(filename, 'utf8');
};


module.exports = [
  {
    pattern: '(.*)',

    fixtures: function(match, params, headers) {
      switch (match[1]) {
        case '/contest/all-lineups/2':
          return require('./hexbytes/contest--all-lineups--2.txt');
        case '/contest/all-lineups/12381281':
          throw new Error(404);
        // TODO LiveContestsStoreConfig - fix data to be from actual call
        case '/contest/info/2':
          return require('./json/contest--info--2');
        case '/contest/info/12381281':
          throw new Error(404);

        case '/draft-group/1/':
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
