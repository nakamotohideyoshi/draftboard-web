import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'

import * as AppActions from '../../stores/app-state-store'
import { updateLiveMode } from '../../actions/live'
import store from '../../store'


/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
var LiveContestsPane = React.createClass({

  propTypes: {
    lineupInfo: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func
  },


  viewContest: function() {
    this.props.updateLiveMode('contest', 2)
  },


  closePane: function() {
    AppActions.removeClass('appstate--live-contests-pane--open')
  },


  render: function() {
    return (
      <div className="live-contests-pane live-pane live-pane--right">
        <div className="live-pane__close" onClick={this.closePane}></div>

        <div className="live-contests-pane__view-contest" onClick={this.viewContest}></div>
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
