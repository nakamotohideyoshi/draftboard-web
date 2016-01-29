import React from 'react';
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx';


/**
 *   Responsible for rendering the horizontal slider.
 *
 * Expects for its children to have a list of elements with class
 * `.scroll-item` and scrolls between them.
 */
const NavScoreboardSlider = React.createClass({

  propTypes: {
    children: React.PropTypes.element,
    type: React.PropTypes.string,
  },

  componentDidMount() {
    this.handleResetScroll();
  },

  componentDidUpdate(prevProps) {
    const oldType = prevProps.type;
    const newType = this.props.type;

    if (oldType !== newType) {
      this.handleResetScroll();
    }
  },

  /**
   * Returns the left position of the slider content holder.
   * @return {Number}
   */
  getContentLeft() {
    const content = this.refs.content;
    let left = content.style.left;

    if (left) {
      left = parseInt(left, 10);
    } else {
      left = 0;
    }

    return left;
  },


  /**
   * Calculates and returns the new scroll position of the slider.
   * @param {Number} direction +1 or -1
   * @return {Number} calculated scroll position
   */
  getNextScrollPosition(direction) {
    const scrollItems = this.refs.content.getElementsByClassName('scroll-item');

    if (this.scrollItem === null) {
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

  /**
   * Scrolls slider left.
   */
  handleScrollLeft() {
    this.refs.content.style.left = `${this.getNextScrollPosition(-1)}px`;
  },

  /**
   * Scrolls slider right.
   */
  handleScrollRight() {
    let left = this.getNextScrollPosition(1);

    const content = this.refs.content;
    const minLeft = content.clientWidth - content.scrollWidth;

    if (left < minLeft) {
      left = minLeft;
      this.getNextScrollPosition(-1);
    }

    content.style.left = `${left}px`;
  },

  /**
   * Reset the scroll position.
   */
  handleResetScroll() {
    this.scrollItem = 0;
    this.refs.content.style.left = '0px';
  },

  render() {
    return (
      <div className="cmp-nav-scoreboard--slider">
        <div className="arrow">
          <NavScoreboardSeparator />
          <div className="left-arrow-icon"
            onClick={this.handleScrollLeft}
          />
          <NavScoreboardSeparator />
          <div className="cmp-nav-scoreboard--shadow"></div>
        </div>
        <div className="slider-content">
          <div className="slider-content--holder" ref="content">
            {this.props.children}
          </div>
        </div>
        <div className="arrow right">
          <NavScoreboardSeparator />
          <div className="right-arrow-icon"
            onClick={this.handleScrollRight}
          />
          <NavScoreboardSeparator />
          <div className="cmp-nav-scoreboard--shadow right"></div>
        </div>
      </div>
    );
  },

});


export default NavScoreboardSlider;
