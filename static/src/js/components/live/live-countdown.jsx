import React from 'react'
import CountdownClock from '../site/countdown-clock'
import { vsprintf } from 'sprintf-js'


const LiveCountdown = React.createClass({

  propTypes: {
    lineup: React.PropTypes.object.isRequired
  },

  getInitialState() {
    return {showMe: true}
  },

  closeCountdown() {
    this.setState({showMe: false})
  },

  render: function() {
    const { name, start } = this.props.lineup
    const editLineup = vsprintf('/draft/%d/lineup/%d/edit/', [this.props.lineup.draftGroup.id, this.props.lineup.id])

    // if timer is out close the countdown
    if (!this.state.showMe) { return null }

    return (
      <div className='live-countdown'>
        <div className='live-countdown__content'>
          <div className='live-countdown__inner'>
            <div className='live-countdown__inner__lineup-name'>{name}</div>
            <div className='live-countdown__inner__startsin'>
              <div>Starts in</div>
              <CountdownClock
                time={start}
                onCountdownOver={ this.closeCountdown } />
            </div>
            <div className='live-countdown__inner__actions'>
              <a href={ editLineup } className="button--medium--outline">Edit Lineup</a>
              <a href="/lobby/" className="button--medium--outline">Edit Contests</a>
            </div>
          </div>
        </div>
      </div>
    )
  }
})


export default LiveCountdown;
