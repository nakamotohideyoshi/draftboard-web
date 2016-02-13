import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';


const ResultsStats = React.createClass({

  propTypes: {
    stats: React.PropTypes.shape({
      winnings: React.PropTypes.string.isRequired,
      possible: React.PropTypes.string.isRequired,
      buyins: React.PropTypes.string.isRequired,
      entries: React.PropTypes.number.isRequired,
      contests: React.PropTypes.number.isRequired,
    }).isRequired,
  },

  mixins: [PureRenderMixin],

  render() {
    return (
      <div className="results-page--stats">
        <div className="item winnings">
          <span className="title">Winnings</span>
          <span className="value">
            ${this.props.stats.winnings}
          </span>
        </div>
        <div className="item possible">
          <span className="title">Possible</span>
          <span className="value">
            ${this.props.stats.possible}
          </span>
        </div>
        <div className="item buyins">
          <span className="title">Fees</span>
          <span className="value">
            ${this.props.stats.buyins}
          </span>
        </div>
        <div className="item entries">
          <span className="title">Entries</span>
          <span className="value">
            {this.props.stats.entries}
          </span>
        </div>
        <div className="item contests">
          <span className="title">Contests</span>
          <span className="value">
            {this.props.stats.contests}
          </span>
        </div>
      </div>
    );
  },

});


export default ResultsStats;
