'use strict';

var React = require('react');
var RangeSlider = require('../form-field/range-slider.jsx');
var ContestActions = require('../../actions/contest-actions');


var ContestListFeeFilter = React.createClass({

  propTypes: {
    className: React.PropTypes.string.isRequired,
    // filterName is used in the ContestStore to store the active filter so other components can
    // reference it. ContestStore.data.filters[{filterName}]
    filterName: React.PropTypes.string.isRequired
  },


  getInitialState: function() {
    return {
      'match': {}
    };
  },


  componentDidMount: function() {
    // Register this filter with the ContestStore.
    ContestActions.registerFilter(this);
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
      ContestActions.filterUpdated(
        this.props.filterName,
        // TODO: Make the column dynamic based on the 'props.property'
        {title: this.props.filterName,
          column: 'fee',
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


module.exports = ContestListFeeFilter;
