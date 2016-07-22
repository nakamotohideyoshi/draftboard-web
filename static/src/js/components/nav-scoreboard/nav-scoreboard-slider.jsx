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

    const isScrollableNow = this.isScrollable();

    if (isScrollableNow !== this.isScrollableVal) {
      this.isScrollableVal = isScrollableNow;
      this.forceUpdate();
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

    // if there are no other items yet is still trying to scroll, return 0
    if (!scrollItems[this.scrollItem]) return 0;

    return -1 * scrollItems[this.scrollItem].offsetLeft;
  },

  /**
   * Scrolls slider left.
   */
  handleScrollLeft() {
    if (!this.isScrollableVal) return;

    this.refs.content.style.left = `${this.getNextScrollPosition(-1)}px`;
  },

  /**
   * Scrolls slider right.
   */
  handleScrollRight() {
    if (!this.isScrollableVal) return;

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

  /**
   * Reset the scroll position.
   */
  isScrollable() {
    const outer = this.refs.content;
    const inner = this.refs.content.children[0];
    return inner && inner.offsetWidth > outer.offsetWidth;
  },

  render() {
    const scrollableClass = this.isScrollableVal ? '' : ' not-scrollable';

    if (!this.props.children || this.props.children.length === 0) {
      return (
        <div className="cmp-nav-scoreboard--slider">
          <div ref="content" />
        </div>
      );
    }

    return (
      <div className="cmp-nav-scoreboard--slider">
        <div className={`arrow left${scrollableClass}`} onClick={this.handleScrollLeft}>
          <NavScoreboardSeparator />
          <svg
            className="icon icon-arrow left-arrow-icon"
            height="10"
            viewBox="0 0 16 16"
            width="10"
          >
            <g>
              <line strokeWidth="2.5" x1="10.3" y1="2.3" x2="4.5" y2="8.1" />
              <line strokeWidth="2.5" x1="3.6" y1="7.3" x2="10.1" y2="13.8" />
            </g>
          </svg>
          <NavScoreboardSeparator />
          <div className="cmp-nav-scoreboard--shadow"></div>
        </div>
        <div className={`slider-content${scrollableClass}`}>
          <div className="slider-content--holder" ref="content">
            {this.props.children}
          </div>
        </div>
        <div className={`arrow right${scrollableClass}`} onClick={this.handleScrollRight}>
          <NavScoreboardSeparator />
          <svg
            className="icon icon-arrow right-arrow-icon"
            height="10"
            viewBox="0 0 16 16"
            width="10"
          >
            <g>
              <line strokeWidth="2.5" x1="10.3" y1="2.3" x2="4.5" y2="8.1" />
              <line strokeWidth="2.5" x1="3.6" y1="7.3" x2="10.1" y2="13.8" />
            </g>
          </svg>
          <NavScoreboardSeparator />
          <div className="cmp-nav-scoreboard--shadow right"></div>
        </div>
      </div>
    );
  },

});


export default NavScoreboardSlider;
