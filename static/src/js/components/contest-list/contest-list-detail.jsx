import React from 'react'
import {Provider, connect} from 'react-redux';
import store from '../../store'
import renderComponent from '../../lib/render-component';


/**
 * Renders a <tr> containing the payout structure details of the selected contest.
 */
var ContestListDetail = React.createClass({

  propTypes: {
    contest: React.PropTypes.object
  },

  getContest: function() {
    if(this.props.contest) {
      return (
        <div>
          <div className="cmp-contest-list__detail-inner">
            <h2 className="cmp-contest-list__detail__name">
              {this.props.contest.name}
            </h2>

            <h6>Live In</h6>
            <h3>{this.props.contest.start}</h3>
            <span>Prize Pool: ${this.props.contest.prize_pool}</span>
            <span>Fee: ${this.props.contest.buyin}</span>
            <span>Entrants: {this.props.contest.current_entries} / {this.props.contest.entries}</span>
          </div>

          <div colSpan="9" className="cmp-contest-list__cell" key="details">
            <div className="col col-1">
              <h4 className="cmp-contest-list__detail-header">Payout Structure</h4>
              <ul>
                <li>1st - $100</li>
                <li>2st - $60</li>
                <li>3st - $40</li>
                <li>4st - $30</li>
                <li>5st - $10</li>
                <li>2st - $60</li>
                <li>3st - $40</li>
                <li>4st - $30</li>
                <li>5st - $10</li>
              </ul>
            </div>

            <div className="col col-2">
              <h4 className="cmp-contest-list__detail-header">NBA Scoring</h4>
              <ul>
                <li>1st - $100</li>
                <li>2st - $60</li>
                <li>3st - $40</li>
                <li>4st - $30</li>
                <li>5st - $10</li>
                <li>2st - $60</li>
                <li>3st - $40</li>
                <li>4st - $30</li>
                <li>5st - $10</li>
              </ul>
            </div>
          </div>
        </div>
      )
    }
    else {
      return (
        <div>Select a Contest</div>
      )
    }
  },

  render: function() {
    let contestDetail = this.getContest();

    return (
      <div className="cmp-contest-list__detail">
        {contestDetail}
      </div>
    )
  }

})




// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    contest: state.upcomingContests.allContests[state.upcomingContests.focusedContestId]
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    // focusPlayer: (playerId) => dispatch(setFocusedPlayer(playerId)),
  };
}

// Wrap the component to inject dispatch and selected state into it.
var ContestListDetailConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(ContestListDetail);

renderComponent(
  <Provider store={store}>
    <ContestListDetailConnected />
  </Provider>,
  '.cmp-contest-list-detail'
);


module.exports = ContestListDetailConnected;
