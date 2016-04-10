import thunk from 'redux-thunk';
import { applyMiddleware, createStore } from 'redux';
import { browserHistory } from 'react-router';
import { logger } from '../lib/logging';
import { routerMiddleware } from 'react-router-redux';

const routerHistory = routerMiddleware(browserHistory);

/**
 * Responsible for combining all the system's middlewares in a single place.
 */
export default applyMiddleware(thunk, logger, routerHistory)(createStore);
