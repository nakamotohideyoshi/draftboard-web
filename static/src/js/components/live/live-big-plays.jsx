import React from 'react';
import LiveBigPlay from './live-big-play';

// assets
require('../../../sass/blocks/live/live-big-plays.scss');

const ITEMS_PER_PAGE = 3;

export default React.createClass({

  propTypes: {
    queue: React.PropTypes.array.isRequired,
  },

  getInitialState() {
    return {
      pointer: 1,
    };
  },

  componentWillReceiveProps(nextProps) {
    // Advance the pointer forward if the user is looking at the most recent play.
    if (this.state.pointer === this.props.queue.length) {
      this.setState({ pointer: nextProps.queue.length });
    }
  },

  /**
   * Returns the current page's items from the queue.
   */
  getCurPage() {
    if (this.state.pointer < ITEMS_PER_PAGE) {
      return this.props.queue;
    }

    const itemsPerPage = Math.min(this.props.queue.length, ITEMS_PER_PAGE);
    const stop = this.state.pointer;
    const start = this.state.pointer - itemsPerPage;

    return this.props.queue.slice(start, stop);
  },

  /**
   * Moves the queue forward one place.
   */
  next() {
    if (this.hasNext()) {
      this.setState({ pointer: this.state.pointer + 1 });
    }
  },

  /**
   * Moves the queue backwards one place.
   */
  prev() {
    if (this.hasPrev()) {
      this.setState({ pointer: this.state.pointer - 1 });
    }
  },

  /**
   * Returns true if the queue can be moved forwards.
   */
  hasNext() {
    const maxPointer = this.props.queue.length;
    return this.props.queue.length > ITEMS_PER_PAGE && this.state.pointer < maxPointer;
  },

  /**
   * Returns true if the queue can be moved backwards.
   */
  hasPrev() {
    const minPointer = Math.min(this.props.queue.length, ITEMS_PER_PAGE);
    return this.props.queue.length > ITEMS_PER_PAGE && this.state.pointer > minPointer;
  },

  render() {
    return (
      <section className="live-big-plays">
        <button className="btn-prev" disabled={ !this.hasPrev() } onClick={ this.prev }>&lt;</button>
        <div className="live-big-plays__items">
          { this.getCurPage().map(pbp =>
              <LiveBigPlay key={pbp.id} event={pbp} />)
          }
        </div>
        <button className="btn-next" disabled={ !this.hasNext() } onClick={ this.next }>&gt;</button>
      </section>
    );
  },

});
