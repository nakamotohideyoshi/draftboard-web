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
import 'mock-local-storage';
import testDom from '../test/test-dom.js';
testDom();
