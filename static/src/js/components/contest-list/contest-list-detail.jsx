import React from 'react'
import {Provider, connect} from 'react-redux';
import store from '../../store'
import renderComponent from '../../lib/render-component';
import PrizeStructure from './prize-structure.jsx'
import {enterContest, setFocusedContest} from '../../actions/upcoming-contests-actions.js'
import {timeRemaining} from '../../lib/utils.js'
import * as AppActions from '../../stores/app-state-store.js'
import { Router, Route } from 'react-router'
import {updatePath, syncReduxAndRouter} from 'redux-simple-router'
import createBrowserHistory from 'history/lib/createBrowserHistory'

const history = createBrowserHistory()
syncReduxAndRouter(history, store)


/**
 * Renders a slideout pane with details of the selected contest.
 */
var ContestListDetail = React.createClass({

  propTypes: {
    contest: React.PropTypes.object,
    prizeStructure: React.PropTypes.object,
    enterContest: React.PropTypes.func,
    focusedLineupId: React.PropTypes.number,
    focusedContestId: React.PropTypes.oneOfType([React.PropTypes.number, React.PropTypes.string]),
    params: React.PropTypes.object,
    setFocusedContest: React.PropTypes.func
  },


  /**
   * When we get new props, check to see if the focusedContestId is the same as the id in the URL.
   * if it isn't, set what's in the URL as the focused contest and open the side panel to view it.
   */
  componentWillReceiveProps: function(nextProps) {
    if (nextProps.params.contestId && this.props.focusedContestId !== nextProps.params.contestId) {
      this.props.setFocusedContest(nextProps.params.contestId)
      AppActions.openPane();
    }
  },


  getInitialState: function() {
    return {
      activeTab: 'prizes'
    }
  },

  // Enter the currently focused lineup into a contest.
  handleEnterContest: function(contestId) {
    this.props.enterContest(contestId, this.props.focusedLineupId)
  },


  // Get the content of the selected tab.
  getActiveTab: function() {
    switch (this.state.activeTab) {
      case 'prizes':
        return (<PrizeStructure structure={this.props.prizeStructure} />)

      case 'scoring':
        return 'scoring tab'

      case 'games':
        return 'games tab'

      case 'entries':
        return 'entries tab'

      default:
        return ('Select a tab')
    }
  },


  // When a tab is clicked, tell the state to show it'scontent.
  handleTabClick: function(tabName) {
    this.setState({'activeTab': tabName})
  },


  // I know making these their own components would be more 'react', but I don't want to deal with
  // the hassle right now.
  getTabNav: function() {
    const tabs = [
      {title: 'Payout', tab: 'prizes'},
      {title: 'Scoring', tab: 'scoring'},
      {title: 'Games', tab: 'games'},
      {title: 'Entries', tab: 'entries'}
    ]

    return tabs.map(function(tab) {
      let classes = ''

      if (this.state.activeTab === tab.tab) {
        classes = 'active'
      }

      return (
        <li key={tab.tab} className={classes} onClick={this.handleTabClick.bind(this, tab.tab)}>{tab.title}</li>
      )
    }.bind(this))
  },


  getContest: function() {
    if(this.props.contest) {
      let tabNav = this.getTabNav()
      let liveIn = timeRemaining(this.props.contest.start)

      return (
        <div>
          <div className="cmp-contest-list__detail-inner">
            <div className="cmp-contest-list__detail-upper">
              <h2 className="cmp-contest-list__detail__name">
                {this.props.contest.name}
              </h2>

              <h6>Live In</h6>

              <h3>{liveIn.hours}:{liveIn.minutes}:{liveIn.seconds}</h3>

              <div className="contest-info">
                <span>Prize Pool: ${this.props.contest.prize_pool.toFixed(2)}</span>
                <span>Fee: ${this.props.contest.buyin.toFixed(2)}</span>
                <span>Entrants: {this.props.contest.current_entries} / {this.props.contest.entries}</span>
              </div>

              <div
                className="button button--gradient button--medium"
                onClick={this.handleEnterContest.bind(null, this.props.focusedLineupId)}
              >
                Enter Contest
              </div>
            </div>
          </div>

          <div colSpan="9" className="cmp-contest-list__detail-lower">
            <ul className="tab-nav">{tabNav}</ul>
            <div className="tab-content">{this.getActiveTab()}</div>
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



function mapStateToProps(state) {
  // TODO: put this in a reusable selector.
  let contest = state.upcomingContests.allContests[state.upcomingContests.focusedContestId]
  let prizeStructure = null

  if (contest && contest.hasOwnProperty('prize_structure')) {
    prizeStructure = state.prizes[contest.prize_structure]
  }

  return {
    contest,
    focusedContestId: state.upcomingContests.focusedContestId,
    prizeStructure,
    focusedLineupId: state.upcomingLineups.focusedLineupId
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    enterContest: (contestId, lineupId) => dispatch(enterContest(contestId, lineupId)),
    setFocusedContest: (contestId) => dispatch(setFocusedContest(contestId))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var ContestListDetailConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(ContestListDetail);

renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/lobby/" component={ContestListDetailConnected} />
      <Route path="/lobby/:contestId/" component={ContestListDetailConnected} />
    </Router>
  </Provider>,
  '.cmp-contest-list-detail'
);


module.exports = ContestListDetailConnected
