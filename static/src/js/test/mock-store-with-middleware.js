// mock store
import api from '../middleware/api';
import configureStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import { browserHistory } from 'react-router';
import { logger } from '../lib/logging';
import { routerMiddleware } from 'react-router-redux';

const routerHistory = routerMiddleware(browserHistory);
const middlewares = [api, thunk, logger, routerHistory]; // add your middlewares like `redux-thunk`

export default configureStore(middlewares);
