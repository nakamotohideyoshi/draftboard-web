import Odometer from '../../lib/odometer';
import React from 'react';
import ReactDOM from 'react-dom';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';

// assets
require('../../../sass/blocks/site/odometer.scss');


/**
 * React housing around Hubspot Odometer plugin
 * Used to animate numbers
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
export default React.createClass({

  propTypes: {
    value: React.PropTypes.number.isRequired,
    modifiers: React.PropTypes.array,
  },

  getDefaultProps() {
    return {
      modifiers: [],
    };
  },

  componentDidMount() {
    // make sure that Odometer doesn't go looking for other similarly named DOM nodes
    window.odometerOptions = {
      auto: false,
    };

    this.odometer = new Odometer({
      el: ReactDOM.findDOMNode(this),  // attaches to the rendered div
      value: 0,
    });

    this.odometer.update(this.props.value);
  },

  componentDidUpdate() {
    this.odometer.update(this.props.value);
  },

  render() {
    const { modifiers } = this.props;

    const block = 'odometer';
    const classNames = generateBlockNameWithModifiers(block, modifiers);

    return (
      <div className={classNames} />
    );
  },
});
