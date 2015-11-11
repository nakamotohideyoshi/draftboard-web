'use strict';


// custom txt require as string, solved by http://goo.gl/ZmalV3
const fs = require('fs');
require.extensions['.txt'] = function (module, filename) {
    module.exports = fs.readFileSync(filename, 'utf8');
};


module.exports = [
  {
    pattern: '(.*)',

    fixtures: function(match, params, headers) {
      switch (match[1]) {
        case '/contest/current-entries/':
          return require('./json/contest--current-entries.json');

        case '/contest/all-lineups/2':
          return require('./hexbytes/contest--all-lineups--2.txt');
        case '/contest/info/2':
          return require('./json/contest--info--2');

        case '/draft-group/1/':
          return require('./json/draft-group--1.json');
        case '/draft-group/fantasy-points/1':
          return require('./json/draft-group--fantasy-points--1.json');
        case '/draft-group/box-scores/1':
          return require('./json/draft-group--box-scores--1.json');
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
