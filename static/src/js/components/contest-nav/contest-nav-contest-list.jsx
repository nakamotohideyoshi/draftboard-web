'use strict';

var React = require('react');
var ContestNavContest = require('./contest-nav-contest.jsx');

var ContestNavContestList = React.createClass({

  propTypes: {
    contests: React.PropTypes.array
  },

  getInitialState: function() {
    return {
      carouselIndex: 0
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

    this.setState({
      contestElementWidth: contestWidth
    });
  },

  showNext: function() {
    console.log('shownext()');
  },

  showPrevious: function() {
    console.log('showprevious()');
  },

  render: function() {
    // console.log(this.props.contests);

    var contests = this.props.contests.map(function(contest) {
      return (
        <ContestNavContest contest={contest} key={contest.id} />
      );
    });

    return (
      <div className="cmp-contest-nav--contests">
        <ul className="cmp-contest-nav--contests-list" ref="contestList">
          {contests}
        </ul>

        <div className="cmp-contest-nav--prev cmp-contest-nav--control" onClick={this.showPrevious}>&lt;</div>
        <div className="cmp-contest-nav--next cmp-contest-nav--control" onClick={this.showNext}>&gt;</div>
      </div>
    );
  }

});


module.exports = ContestNavContestList;
