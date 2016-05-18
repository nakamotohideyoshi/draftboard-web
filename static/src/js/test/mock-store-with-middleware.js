// mock store
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import { browserHistory } from 'react-router';
import { logger } from '../lib/logging';
import { routerMiddleware } from 'react-router-redux';

const routerHistory = routerMiddleware(browserHistory);
const middlewares = [thunk, logger, routerHistory]; // add your middlewares like `redux-thunk`

export default configureStore(middlewares);
