console.log(`\n
╔══════════════════════ ೋღ☃ღೋ  ═════════════════════╗
~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
~ ~ ~ Bootstrapping test suite via bootstrap.js ~ ~ ~
~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
╚══════════════════════ ೋღ☃ღೋ  ═════════════════════╝
\n\n`);

/**
 * Load up localstorage + browser dom + window mocks.
 */
import 'babel-core/register';
import 'babel-polyfill';
import 'mock-local-storage';
import testDom from '../test/test-dom.js';
testDom();
