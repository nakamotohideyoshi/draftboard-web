import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import { map as _map } from 'lodash'

import * as AppActions from '../../stores/app-state-store'
import { updateLiveMode } from '../../actions/live'
import store from '../../store'


/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
var LiveContestsPane = React.createClass({

  propTypes: {
    liveContests: React.PropTypes.object.isRequired,
    currentLineups: React.PropTypes.object.isRequired,
    lineupInfo: React.PropTypes.object.isRequired,
    prizes: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func
  },


  viewContest: function(id) {
    this.props.updateLiveMode('contest', id)
  },


  closePane: function() {
    AppActions.removeClass('appstate--live-contests-pane--open')
  },


  render: function() {
    let self = this;

    if (self.props.lineupInfo.id in self.props.currentLineups.items === false) {
      return (<div className="live-contests-pane live-pane live-pane--right" />)
    }

    const moneyLine = (
      <section className="live-winning-graph">
        <div className="live-winning-graph__pmr-line">
          <span style={{ width: '20%'}}></span>
        </div>
      </section>
    )

    const lineup = self.props.currentLineups.items[self.props.lineupInfo.id]
    let lineupContests = _map(lineup.contests, function(key) {
      const contest = self.props.liveContests[key]

      return (
        <li className="live-contests-pane__contest" key={ contest.id }>
          <div className="live-contests-pane__name">{ contest.info.name }</div>
          <div className="live-contests-pane__place">
            <span className="live-contests-pane__place--mine">22</span> of 2,932
          </div>
          <div className="live-contests-pane__potential-earnings">${ contest.info.buyin }/$80</div>
          { moneyLine }

          <div className="live-contest-cta" onClick={ self.viewContest.bind(self, contest.id) }>Watch Live</div>
        </li>
      )
    })


    return (
      <div className="live-contests-pane live-pane live-pane--right">
        <div className="live-pane__close" onClick={self.closePane} />

        <div className="live-pane__content">
          <h2>
            My Contests
          </h2>

          <div className="live-contests-pane__list">
            <ul className="live-contests-pane__list__inner">
              { lineupContests }
            </ul>
          </div>
        </div>
        <div className="live-pane__left-shadow" />

        <div className="live-contests-pane__view-contest" onClick={self.viewContest} />
      </div>
    )
  }
})


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {}
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (type, id) => dispatch(updateLiveMode(type, id))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveContestsPaneConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveContestsPane)

// Render the component.
renderComponent(
  <Provider store={store}>
    <LiveContestsPaneConnected />
  </Provider>,
  '.live-contests-pane'
)


module.exports = LiveContestsPaneConnected
