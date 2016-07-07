import ReactDOM from 'react-dom';
import log from './logging';

// get custom logger for actions
const logComponent = log.getLogger('component');


/**
 * Render a React Component to all instances of the given DOM selector.
 * @param  {string} selector  A css-style dom selector.
 * @param  {Object} component A React comopnent instance.
 */
export default (component, selector) => {
  // Query all matching DOM elements.
  const elements = document.querySelectorAll(selector);

  Array.from(elements).forEach((element) => {
    logComponent.debug('Rendering component on:', selector);
    ReactDOM.render(component, element);
  });
};
