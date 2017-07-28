import React from 'react';
import { CSSTransitionGroup } from 'react-transition-group';
import LiveHistoryListPBP from './live-history-list-pbp';

// assets
require('../../../sass/blocks/live/live-history-list.scss');

// BEM class name
const block = 'live-history-list';

export default React.createClass({

  propTypes: {
    currentEvent: React.PropTypes.object,
  },

  getInitialState() {
    return {
      offset: 0,
      curEvent: null,
      history: [],
    };
  },

  componentWillReceiveProps(nextProps) {
    const curEvent = this.state.curEvent;
    const nextEvent = nextProps.currentEvent;

    // If we are not receiving a new event, or waiting for a curEvent to expire
    // exit the update.
    if (curEvent && !nextEvent) {
      this.setState({
        offset: this.state.offset + (this.state.offset > 0 ? 1 : 0),
        history: this.state.history.concat([curEvent]),
      });
    }

    this.setState({ curEvent: nextEvent });
  },

  /**
   * Returns the current page's items from the queue.
   */
  getCurrentItems() {
    const { history, offset } = this.state;

    const len = this.state.history.length;
    const itemsPerPage = 10;
    const numPages = len / itemsPerPage;

    let start = 0;
    let end = len - offset;

    if (numPages > 1) {
      start = Math.max(0, (len - itemsPerPage) - offset);
      end = Math.max(start, (start + itemsPerPage) - offset);
    }

    return history.slice(start, end);
  },

  /**
   * Moves the queue forward one place.
   */
  next() {
    if (this.hasNext()) {
      this.setState({
        offset: Math.max(0, this.state.offset - 1),
      });
    }
  },

  /**
   * Moves the queue backwards one place.
   */
  prev() {
    if (this.hasPrev()) {
      const numItems = this.state.history.length;
      this.setState({
        offset: Math.min(numItems - 1, this.state.offset + 1),
      });
    }
  },

  /**
   * Returns true if the queue can be moved forwards.
   */
  hasNext() {
    return this.state.offset > 0 && this.state.history.length > 1;
  },

  /**
   * Returns true if the queue can be moved backwards.
   */
  hasPrev() {
    return this.state.offset < this.state.history.length - 1;
  },

  /**
   * Renders a list of LiveHistoryListPBP DOM elements based on array of
   * plays provided.
   */
  renderItems(plays, hasActivity = false) {
    const spaceBetweenItems = 10;
    const activityIndicatorWidth = 50;

    // Calculate the item's position in reverse to ensure that the DOM is
    // stacked appropriately and the items are correctly positioned. Each item
    // is positioned based on its index and the amount of margin applied
    // between items. Additionally, a little offset is given if `hasActivity`
    // is set to `true`.

    return plays.map((pbp, i, arr) => {
      const index = (arr.length - 1) - i;
      const start = hasActivity ? activityIndicatorWidth : 0;
      const margins = index * spaceBetweenItems;
      const calc = `calc(${index * -100}% - ${start + margins}px)`;
      const style = { transform: `translateX(${calc})` };

      let className = `${block}__list-item`;

      if (index === 0) {
        className += ` ${block}__list-item--active`;
      }

      return (
        <div key={pbp.id} {...{ className, style }}>
          <LiveHistoryListPBP event={pbp} />
        </div>
      );
    });
  },

  render() {
    const transitionName = 'item';
    const transitionEnterTimeout = 330;
    const transitionLeaveTimeout = 330;

    let classNames = block;

    if (this.props.currentEvent) {
      classNames += ` ${block}--has-activity`;
    }

    return (
      <section className={classNames}>
        <button className="btn-prev" disabled={ !this.hasPrev() } onClick={ this.prev }>&lt;</button>
        <button className="btn-next" disabled={ !this.hasNext() } onClick={ this.next }>&gt;</button>
        <div className={`${block}__list`}>
          <CSSTransitionGroup {...{ transitionName, transitionEnterTimeout, transitionLeaveTimeout }}>
            {this.renderItems(this.getCurrentItems(), this.props.currentEvent !== null)}
          </CSSTransitionGroup>
        </div>
        { this.props.currentEvent !== null &&
          <div className={`${block}__activity-indicator`}></div>
        }
      </section>
    );
  },

});
