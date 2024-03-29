/**
 * This is really stupid... Unless you're using Gulp + a plugin, Istanbul doesn't automatically
 * see all of your files to determine the test coverage of them, it only looks at the ones that
 * get loaded in the tests. To have it take all of our files into consideration we have to manually
 * require them. This uses the require-dir module to load in all of our files.
 */


import requireDir from 'require-dir';

requireDir('../actions', { recurse: true });
requireDir('../components', { recurse: true });
requireDir('../lib', { recurse: true });
requireDir('../selectors', { recurse: true });
requireDir('../reducers', { recurse: true });
requireDir('../simulations', { recurse: true });
requireDir('../middleware', { recurse: true });
