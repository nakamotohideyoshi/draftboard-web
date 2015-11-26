import React from 'react'
import renderComponent from '../../lib/render-component'

import * as AppActions from '../../stores/app-state-store'


/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
var LiveStandingsPane = React.createClass({


  getInitialState: function() {
    return {
      currentTab: 'standings'
    };
  },


  viewOwnership: function() {
    this.setState({ currentTab: 'ownership' })
  },


  viewStandings: function() {
    this.setState({ currentTab: 'standings' })
  },


  closePane: function() {
    AppActions.removeClass('appstate--live-standings-pane--open')
  },


  render: function() {
    let classNames = 'live-standings-pane live-pane live-pane--right live-standings-pane--' + this.state.currentTab

    return (
      <div className={classNames}>
        <div className="live-pane__close" onClick={this.closePane}></div>

        <div className="live-standings-pane__view-standings" onClick={this.viewStandings}></div>
        <div className="live-standings-pane__view-ownership" onClick={this.viewOwnership}></div>
      </div>
    )
  }
})


// Render the component.
renderComponent(
  <LiveStandingsPane />,
  '.live-standings-pane'
)


module.exports = LiveStandingsPane
