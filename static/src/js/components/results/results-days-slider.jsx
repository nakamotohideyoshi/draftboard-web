'use strict';

import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';

import SmoothScrollTo from '../../lib/smooth-scroll-to.js';
import {getDaysForMonth, weekdayNumToName} from '../../lib/time.js';

const ResultsDaysSlider = React.createClass({

  mixins: [PureRenderMixin],

  propTypes: {
    year: React.PropTypes.number.isRequired,
    month: React.PropTypes.number.isRequired,
    day: React.PropTypes.number.isRequired,
    onSelectDate: React.PropTypes.func.isRequired
  },

  getItemsList() {
    return getDaysForMonth(this.props.year, this.props.month).map(d => {
      return {
        id:       d.toString(),
        daynum:   d.getDate(),
        weekday:  weekdayNumToName(d.getDay()),
        selected: d.getDate() === this.props.day
      };
    });
  },

  handleSelectDate(day) {
    this.props.onSelectDate(this.props.year, this.props.month, day);
  },

  /**
   * Returns current left position of the slider.
   * @return {Number}
   */
  getCurrentScrollPosition() {
    let content = this.refs.content;
    let left = content.style.left;

    if (left) {
      left = parseInt(left, 10);
    } else {
      left = 0;
    }

    return left;
  },

  /**
   * Calculates and returns the new left position of the slider.
   * @param {Number} direction +1 or -1
   * @return {Number}
   */
  getNextScrollPosition(direction) {
    console.assert(direction === 1 || direction === -1);

    const scrollItems = this.refs.content.getElementsByClassName('item');

    if (this.scrollItem == null) {
      this.scrollItem = 0;
    }

    this.scrollItem += direction;

    if (this.scrollItem < 0) {
      this.scrollItem = 0;
    }

    if (this.scrollItem > scrollItems.length - 1) {
      this.scrollItem = scrollItems.length - 1;
    }

    return -1 * scrollItems[this.scrollItem].offsetLeft;
  },

  handleScrollNext() {
    let left = this.getNextScrollPosition(1);

    const content = this.refs.content;
    const minLeft = content.clientWidth - content.scrollWidth;

    if (left < minLeft) {
      left = minLeft;
      this.getNextScrollPosition(-1);
    }

    content.style.left = left + 'px';
  },

  handleScrollPrev() {
    const left = this.getNextScrollPosition(-1);
    this.refs.content.style.left = left + 'px';
  },

  /**
   * Scrolls slider to selected date.
   */
  handleScrollToSelected() {
    this.scrollItem = this.props.day - 2;
    this.handleScrollNext();
  },

  componentDidUpdate() {
    this.handleScrollToSelected();
  },

  componentDidMount() {
    this.handleScrollToSelected();
  },

  render() {
    const items = this.getItemsList().map(i => {
      return [
        <div key={i.id}
             className={"item" + (i.selected ? " selected" : "")}
             onClick={this.handleSelectDate.bind(this, i.daynum)}>
          {i.weekday}
          <span className="value">{i.daynum}</span>
        </div>
      , <div className="separator" key={i.id+"|s"}>/</div>];
    }).reduce((accum, l) => {
      // Just flatten the array on a single level. Not using lodash here,
      // because this may result in unexpected behavior depending on the
      // rendered React component internal representation.
      return accum.concat.apply(accum, l);
    }, []).slice(0, -1); // Remove last separator.

    return (
      <div className="results-days-slider">
        <div className="arrow-left" onClick={this.handleScrollPrev}>&lt;</div>
        <div className="content-holder">
          <div className="content" ref="content"> {items} </div>
        </div>
        <div className="arrow-right" onClick={this.handleScrollNext}>&gt;</div>
      </div>
    );
  }

});


export default ResultsDaysSlider;
