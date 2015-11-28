// custom txt require as string, solved by http://goo.gl/ZmalV3
// const fs = require('fs')
// require.extensions['.txt'] = function (module, filename) {
//     module.exports = fs.readFileSync(filename, 'utf8')
// }


module.exports = [
  {
    pattern: '(.*)',

    fixtures: (match, params, headers) => {
      switch (match[1]) {
        case '/api/contest/all-lineups/2/':
          return '0000000200080000000101c40010001f0126012d00c9004701ac0000000200b100a801290047012d0011012700c4'
        case '/api/contest/current-entries/':
          return require('./json/contest--current-entries')
        case '/api/contest/info/2/':
          return require('./json/contest--info--2')

        case '/api/draft-group/1/':
          return require('./json/draft-group--1')
        case '/api/draft-group/box-scores/1':
          return require('./json/draft-group--box-scores--1');
        case '/api/draft-group/fantasy-points/1':
          return require('./json/draft-group--fantasy-points--1')

        case '/api/prize/1/':
          return require('./json/prize--1')

        // 404s
        case '/api/contest/info/12381281/':
          throw new Error(404)
        case '/api/contest/all-lineups/12381281/':
          throw new Error(404)

        // used to test that fantasy points do not exist
        case '/api/draft-group/114128/':
          return require('./json/draft-group--1')
      }
    },

    // `match`: result of the resolution of the regular expression
    // `data`: data returns by `fixtures` attribute
    callback: (match, data) => {
      return {
        body: data,
        text: data
      }
    }

  }
]
