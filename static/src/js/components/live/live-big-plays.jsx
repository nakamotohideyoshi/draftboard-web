import React from 'react';
import LiveBigPlay from './live-big-play';
import _ from 'lodash';
import { CSSTransitionGroup } from 'react-transition-group';

// assets
require('../../../sass/blocks/live/live-big-plays.scss');

export default React.createClass({

  propTypes: {
    queue: React.PropTypes.array.isRequired,
    currentEvent: React.PropTypes.object,
  },

  getInitialState() {
    return {
      offset: 0,
      history: [],
    };
  },

  componentWillReceiveProps(nextProps) {
    if (nextProps.history.length > 0) {
      const nextItem = _.last(nextProps.history);
      const prevItem = _.last(this.state.history);

      if (prevItem && nextItem.id === prevItem.id) {
        return;
      }

      this.setState({
        offset: this.state.offset + (this.state.offset > 0 ? 1 : 0),
        history: this.state.history.concat([nextItem]),
      });
    }
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
   * Renders a list of LiveBigPlay DOM elements based on array of plays provided.
   */
  renderBigPlays(plays, hasActivity = false) {
    const block = 'live-big-plays';
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
          <LiveBigPlay event={pbp} />
        </div>
      );
    });
  },

  render() {
    const block = 'live-big-plays';

    let classNames = block;

    if (this.props.currentEvent) {
      classNames += ` ${block}--has-activity`;
    }

    return (
      <section className={classNames}>
        <button className="btn-prev" disabled={ !this.hasPrev() } onClick={ this.prev }>&lt;</button>
        <button className="btn-next" disabled={ !this.hasNext() } onClick={ this.next }>&gt;</button>
        <div className={`${block}__list`}>
          <CSSTransitionGroup transitionName="item" transitionEnterTimeout={500} transitionLeaveTimeout={350}>
            {this.renderBigPlays(this.getCurrentItems(), this.props.currentEvent !== null)}
          </CSSTransitionGroup>
        </div>
        <div className={`${block}__activity-indicator`}></div>
      </section>
    );
  },

});
