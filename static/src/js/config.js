'use strict';

// Default to errors only.
var level = 'error';

// If 'development' or nothing is set, use warn. Stay with 'error' for prod.
if (process.env.NODE_ENV !== 'production') {
  level = 'debug';
}

if (process.env.NODE_ENV === 'test') {
  level = 'warn';
}

module.exports = {
  'logLevel': level
};
