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
/**
 * Note: Any browser globals that are needed get added in the test-dom.js file.
 */
import testDom from '../test/test-dom.js';
testDom();
