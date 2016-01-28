import { applyMiddleware, createStore } from 'redux';
import thunk from 'redux-thunk';

import { logger } from '../lib/logging';


/**
 * Responsible for combining all the system's middlewares in a single place.
 */
export default applyMiddleware(thunk, logger)(createStore);
