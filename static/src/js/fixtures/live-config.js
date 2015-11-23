// custom txt require as string, solved by http://goo.gl/ZmalV3
// const fs = require('fs')
// require.extensions['.txt'] = function (module, filename) {
//     module.exports = fs.readFileSync(filename, 'utf8')
// }


module.exports = [
  {
    pattern: '(.*)',

    fixtures: (match, params, headers) => {
      // ok this kinda sucks. webpack requires json-loader, tests do not.
      let jsonLoaderPrefix = 'json!'
      if (process.env.NODE_ENV === 'test') {
        jsonLoaderPrefix = ''
      }

      switch (match[1]) {
        case '/contest/all-lineups/2':
          return '0000000200080000000101c40010001f0126012d00c9004701ac0000000200b100a801290047012d0011012700c4'
        case '/contest/current-entries/':
          return require(jsonLoaderPrefix + './json/contest--current-entries.json')
        case '/contest/info/2':
          return require(jsonLoaderPrefix + './json/contest--info--2.json')

        case '/draft-group/1/':
          return require(jsonLoaderPrefix + './json/draft-group--1.json')
        case '/draft-group/box-scores/1':
          return require(jsonLoaderPrefix + './json/draft-group--box-scores--1.json');
        case '/draft-group/fantasy-points/1':
          return require(jsonLoaderPrefix + './json/draft-group--fantasy-points--1.json')

        // 404s
        case '/contest/info/12381281':
          throw new Error(404)
        case '/contest/all-lineups/12381281':
          throw new Error(404)

        // used to test that fantasy points do not exist
        case '/draft-group/114128/':
          return require(jsonLoaderPrefix + './json/draft-group--1.json')
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
