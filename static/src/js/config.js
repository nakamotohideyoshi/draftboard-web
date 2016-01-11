'use strict';

// Default to errors only and prouction
var level = 'error';
var environment = process.env.NODE_ENV || 'production'


if (process.env.NODE_ENV === 'debug') {
  level = 'debug';
}

if (process.env.NODE_ENV === 'test') {
  level = 'warn';
}

// override with URL query param
if (window.dfs.logLevel !== '') {
  level = window.dfs.logLevel
}

module.exports = {
  'logLevel': level
};
