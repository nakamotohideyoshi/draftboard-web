'use strict';


module.exports = [
  {
    pattern: '(.*)',

    fixtures: function(match, params, headers) {
      switch (match[1]) {
        case '/contest/all-lineups/1':
          return '0000000200080000000101bb004d002e004e01c800f7017300000002005b01bb004d002e004e01c800f701730000';
        case '/draft-group/1/':
          return require('./json/live-nba-draft-group.json');
        case '/draft-group/fantasy-points/1':
          return require('./json/live-nba-draft-group-fantasy-points.json');
        case '/contest/single-lineup/1/2':
          return require('./json/live-nba-single-lineup-2.json');
        case '/contest/single-lineup/1/3':
          return require('./json/live-nba-single-lineup-3.json');
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
