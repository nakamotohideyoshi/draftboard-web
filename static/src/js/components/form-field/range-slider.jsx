'use strict';

var React = require('react');
var noUiSlider = require('nouislider');


/**
 * A react wrapper around the noUiSlider library (http://refreshless.com/nouislider/).
 */
var RangeSlider = React.createClass({

  propTypes: {
    minValLimit: React.PropTypes.number.isRequired,
    maxValLimit: React.PropTypes.number.isRequired,
    onChange: React.PropTypes.func.isRequired
  },


  getInitialState: function() {
    return {
      minVal: this.props.minValLimit,
      maxVal: this.props.maxValLimit
    };
  },


  componentDidMount: function() {
    this.slider = React.findDOMNode(this.refs.slider);

    if(this.slider) {
      // Create the slider.
      noUiSlider.create(this.slider, {
        start: [this.state.minVal, this.state.maxVal],
        step: 0.25,
        connect: true,
        range: {
          // Cast as floats in case a string was provided.
          min: parseFloat(this.props.minValLimit),
          max: parseFloat(this.props.maxValLimit)
        }
      });

      // When the slider value change event fires...
      this.slider.noUiSlider.on('slide', function(){
        this.handleValueChange.apply(this, this.slider.noUiSlider.get());
      }.bind(this));
    }
  },


/**
 * New Min + Max values to be passed upwards to the parent component. The callback is for
 * testing purposes since setState is async.
 */
  handleValueChange: function(min, max, callback) {
    callback = callback || function(){};

    this.setState({
      minVal: min,
      maxVal: max
    }, function() {
      this.props.onChange(this.state);
      // Update the value readout. If we ever need this for anyything other than the contest list,
      // this will need to be abstracted out of this component and dynamic via props.
      React.findDOMNode(this.refs.values).innerHTML = "$" + min + " - " + "$" + max;
      callback();
    });
  },


  // After the first render, we don't ever want to overwrite the noUiSlider DOM element. If we did,
  // we'd have to reinstantiate the slider.
  shouldComponentUpdate: function() {
    return false;
  },


  render: function() {
    return (
      <div className="cmp-range-slider">
        <div className="cmp-range-slider__slider" ref="slider"></div>
        <div className="cmp-range-slider__values" ref="values">
          ${this.state.minVal} - ${this.state.maxVal}
        </div>
      </div>
    );
  }

});


module.exports = RangeSlider;
