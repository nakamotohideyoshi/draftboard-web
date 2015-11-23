import React from 'react'
import renderComponent from '../../lib/render-component'

import * as AppActions from '../../stores/app-state-store'


/**
 * When `View Contests` element is clicked, open side pane to show a user's current contests for that lineup.
 */
var LivePlayerPane = React.createClass({

  closePane: function() {
    AppActions.removeClass('appstate--live-player-pane--open')
  },


  render: function() {
    return (
      <div className="live-player-pane live-pane live-pane--left">
        <div className="live-pane__close" onClick={this.closePane}></div>
      </div>
    )
  }
})


// Render the component.
renderComponent(
  <LivePlayerPane />,
  '.live-player-pane'
)


module.exports = LivePlayerPane
