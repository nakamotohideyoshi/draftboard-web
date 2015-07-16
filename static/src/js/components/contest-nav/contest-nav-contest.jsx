'use strict';

var React = require('react');


var ContestNavContest = React.createClass({

  propTypes: {
    contest: React.PropTypes.object
  },

  render: function() {
    return (
      <li className="cmp-contest-nav--contest">
        <a href="#">
          <h5>{this.props.contest.title}</h5>

          <div className="winning">
            <span className="key">Winning</span>
            <span className="value">{this.props.contest.winning}</span>
          </div>

          <div className="position">
            <span className="key">Pos.</span>
            <span className="value">
              <strong>{this.props.contest.position}</strong>/{this.props.contest.entries}
            </span>
          </div>

          <div className="cmp-contest-nav--chart">
            -------------
          </div>
        </a>
      </li>
    );
  }

});


module.exports = ContestNavContest;
