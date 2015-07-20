'use strict';

var React = require('react');
var ContestNavContest = require('./contest-nav-contest.jsx');

var ContestNavContestList = React.createClass({

  propTypes: {
    contests: React.PropTypes.array
  },

  getInitialState: function() {
    return {
      carouselIndex: 0,
      carouselPaneWidth: 0
    };
  },

  getDefaultProps: function() {
    return {
      contests: []
    };
  },

  componentDidMount: function() {
    this.getContestElementWidth();
  },

  componentWillReceiveProps: function() {
    this.getContestElementWidth();
  },

  getContestElementWidth: function() {
    var contestCollection = React.findDOMNode(this.refs.contestList).querySelectorAll('li');
    var contestWidth = contestCollection.length > 0 ? contestCollection[0].offsetWidth : '0px';
    var visibleListWidth = React.findDOMNode(this).offsetWidth;

    this.setState({
      contestElementWidth: contestWidth,
      carouselPaneWidth: Math.floor(visibleListWidth / contestWidth) * contestWidth,
      carouselOffset: 0
    });
  },


  /**
   * Get the contest list 'left' css style property.
   * @return {Int} the 'left' css style property.
   */
  getListLeftOffset: function() {
    var currentLeft = parseInt(React.findDOMNode(this.refs.contestList).style.left);
    // If the left style property isn't set, default to 0.
    if (isNaN(currentLeft)) {
      currentLeft = 0;
    }

    return currentLeft;
  },

  /**
   * Attempt to slide to the next panel in the list. If there are no more, the action is ignored.
   */
  showNext: function() {
    var currentLeft = this.getListLeftOffset();
    var newLeft = (currentLeft - this.state.carouselPaneWidth);

    // If the new offset is bigger than the entire widht of the list, we know we're already at the last pane.
    if (Math.abs(parseInt(newLeft)) > parseInt(React.findDOMNode(this.refs.contestList).offsetWidth)) {
      this.setState({carouselOffset: currentLeft});
    } else {
      this.setState({carouselOffset: newLeft});
      React.findDOMNode(this.refs.contestList).style.left = newLeft + 'px';
    }
  },

  /**
   * Attempt to slide to the previous panel in the list. If there are no more, the action is ignored.
   */
  showPrevious: function() {
    var currentLeft = this.getListLeftOffset();
    var newLeft = (currentLeft + this.state.carouselPaneWidth);

    if (parseInt(newLeft) > 0) {
      this.setState({carouselOffset: currentLeft});
    } else {
      this.setState({carouselOffset: newLeft});
      React.findDOMNode(this.refs.contestList).style.left = newLeft + 'px';
    }
  },

  render: function() {
    // If we're on the first pane, don't show the previous button.
    var contests = this.props.contests.map(function(contest) {
      return (
        <ContestNavContest contest={contest} key={contest.id} />
      );
    });

    var navPrev = '';

    if (parseInt(this.state.carouselOffset) < 0) {
      navPrev = (
        <div
          className="cmp-contest-nav--prev cmp-contest-nav--control"
          onClick={this.showPrevious}
        >&lt;</div>
      );
    }

    return (
      <div className="cmp-contest-nav--contests">
        <ul className="cmp-contest-nav--contests-list" ref="contestList">
          {contests}
        </ul>

        {navPrev}
        <div
          className="cmp-contest-nav--next cmp-contest-nav--control"
          onClick={this.showNext}
        >&gt;</div>
      </div>
    );
  }

});


module.exports = ContestNavContestList;
