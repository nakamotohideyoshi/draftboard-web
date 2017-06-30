/*
* This will create a separate bundle that inludes all necessary assets
* for the live debugger panel. (found at /debug/live-animations/). This
* is done so we don't have to keep all of the debugger assetes in the
* production code that end users download but will never use.
*/

// Load regular full app code
require('./app');

// Add Live Debugger code
require('components/live-debugger/live-debugger');
