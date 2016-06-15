import thunk from 'redux-thunk';
import api from './api';
import { applyMiddleware, createStore, compose } from 'redux';
import { browserHistory } from 'react-router';
import { logger } from '../lib/logging';
import { routerMiddleware } from 'react-router-redux';

const routerHistory = routerMiddleware(browserHistory);

// Responsible for combining all the system's middlewares in a single place.
let middleware = applyMiddleware(thunk, api, logger, routerHistory)(createStore);

// Add in redux devtools if you're developing
if (process.env.NODE_ENV === 'debug' || process.env.NODE_ENV === 'development') {
  middleware = compose(
    applyMiddleware(thunk, api, logger, routerHistory),
    window.devToolsExtension ? window.devToolsExtension() : f => f
  )(createStore);
}

export default middleware;
