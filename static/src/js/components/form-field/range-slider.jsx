import React from 'react';
import ReactDom from 'react-dom';
import noUiSlider from 'nouislider';


/**
 * A react wrapper around the noUiSlider library (http://refreshless.com/nouislider/).
 */
const RangeSlider = React.createClass({

  propTypes: {
    minValLimit: React.PropTypes.number.isRequired,
    maxValLimit: React.PropTypes.number.isRequired,
    onChange: React.PropTypes.func.isRequired,
  },


  getInitialState() {
    return {
      minVal: this.props.minValLimit,
      maxVal: this.props.maxValLimit,
    };
  },


  componentDidMount() {
    const self = this;
    this.slider = ReactDom.findDOMNode(this.refs.slider);

    if (this.slider) {
      // Create the slider.
      noUiSlider.create(this.slider, {
        start: [this.state.minVal, this.state.maxVal],
        step: 0.25,
        connect: true,
        range: {
          // Cast as floats in case a string was provided.
          min: parseFloat(this.props.minValLimit),
          max: parseFloat(this.props.maxValLimit),
        },
      });

      // When the slider value change event fires...
      this.slider.noUiSlider.on('slide', () => {
        self.handleValueChange.apply(self, self.slider.noUiSlider.get());
      });
    }
  },


  // After the first render, we don't ever want to overwrite the noUiSlider DOM element. If we did,
  // we'd have to reinstantiate the slider.
  shouldComponentUpdate() {
    return false;
  },


/**
 * New Min + Max values to be passed upwards to the parent component. The callback is for
 * testing purposes since setState is async.
 */
  handleValueChange: (min, max, callback = () => {''}) => {
    this.setState({
      minVal: min,
      maxVal: max,
    }, () => {
      this.props.onChange(this.state);
      // Update the value readout. If we ever need this for anyything other than the contest list,
      // this will need to be abstracted out of this component and dynamic via props.
      ReactDom.findDOMNode(this.refs.values).innerHTML = `$${min} - $${max}`;
      callback();
    });
  },


  render() {
    return (
      <div className="cmp-range-slider">
        <div className="cmp-range-slider__slider" ref="slider"></div>
        <div className="cmp-range-slider__values" ref="values">
          ${this.state.minVal} - ${this.state.maxVal}
        </div>
      </div>
    );
  },

});


module.exports = RangeSlider;
