'use strict';

var React = require('react');
var RangeSlider = require('../form-field/range-slider.jsx');


var CollectionRangeSliderFilter = React.createClass({

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
    // Once the filter has mounted, it needs to register itself with a store.
    onMount: React.PropTypes.func.isRequired
  },


  getInitialState: function() {
    return {
      'match': {}
    };
  },


  componentDidMount: function() {
    // Register this filter with the Store with the provided function.
    this.props.onMount(this);
  },


  filter: function(row) {
    // Is the property value less than the minimum range value, or greater than the biggest?
    // TODO: make the row property this is checking dynamic based on the 'props.property'
    if (
      row.buyin < this.state.match.minVal ||
      row.buyin > this.state.match.maxVal
    ) {
      return false;
    }

    return true;
  },


  handleChange: function(sliderState) {
    var match = {
      minVal: sliderState.minVal,
      maxVal: sliderState.maxVal
    };

    this.setState({'match': match}, function() {
      this.props.onUpdate(
        this.props.filterName,
        {title: this.props.filterName,
          column: this.props.filterProperty,
          match: {
            minVal: sliderState.minVal,
            maxVal: sliderState.maxVal
          }
        }
      );
    });
  },


  render: function() {
    return (
      <RangeSlider minValLimit={0} maxValLimit={100} onChange={this.handleChange} />
    );
  }

});


module.exports = CollectionRangeSliderFilter;
