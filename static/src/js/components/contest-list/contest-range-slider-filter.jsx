import React from 'react';
import RangeSlider from '../form-field/range-slider.jsx';


const CollectionRangeSliderFilter = React.createClass({

  propTypes: {
    className: React.PropTypes.string,
    // The propety in the row that we are filtering against.
    filterProperty: React.PropTypes.string.isRequired,
    // filterName is used in the datastore to store the active filter so other components can
    // reference it. Store.data.filters[{filterName}]
    filterName: React.PropTypes.string.isRequired,
    // When the filter values have changed, let the store it's registered with know so it can
    // re-run all of it's filters.
    onUpdate: React.PropTypes.func.isRequired,
    minValLimit: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.number,
    ]),
    maxValLimit: React.PropTypes.any,
  },


  getDefaultProps() {
    return {
      minValLimit: 0,
      maxValLimit: null,
    };
  },


  getInitialState() {
    return {
      match: {},
    };
  },


  handleChange(sliderState) {
    const match = {
      minVal: sliderState.minVal,
      maxVal: sliderState.maxVal,
    };

    this.setState({ match }, () => {
      this.props.onUpdate(
        this.props.filterName,
        this.props.filterProperty,
        { minVal: sliderState.minVal, maxVal: sliderState.maxVal }
      );
    });
  },


  render() {
    if (!this.props.maxValLimit) {
      return (
        <div></div>
      );
    }

    return (
      <RangeSlider
        minValLimit={this.props.minValLimit}
        maxValLimit={this.props.maxValLimit}
        onChange={this.handleChange}
      />
    );
  },

});


module.exports = CollectionRangeSliderFilter;
