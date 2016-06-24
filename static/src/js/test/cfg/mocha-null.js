// filetypes unsupported by node need to be returned as null for tests

require.extensions['.scss'] = () => null;
require.extensions['.png'] = () => null;
require.extensions['.jpg'] = () => null;
