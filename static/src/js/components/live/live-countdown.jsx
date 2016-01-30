import React from 'react'

import CountdownClock from '../site/countdown-clock'


const LiveCountdown = React.createClass({

  propTypes: {
    lineup: React.PropTypes.object.isRequired,
    onCountdownComplete: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    return { showMe: true }
  },

  render() {
    const { name, start } = this.props.lineup
    console.warn(this.props.lineup)
    const editLineup = `/draft/${ this.props.lineup.draftGroup.id }/lineup/${ this.props.lineup.id }/edit/`

    return (
      <div className="live-countdown">
        <div className="live-countdown__content">
          <div className="live-countdown__inner">
            <div className="live-countdown__inner__lineup-name">{ name }</div>
            <div className="live-countdown__inner__startsin">
              <div>Starts in</div>
              <CountdownClock
                time={ start }
                onCountdownOver={ this.props.onCountdownComplete }
              />
            </div>
            <div className="live-countdown__inner__actions">
              <a href={ editLineup } className="button--medium--outline">Edit Lineup</a>
              <a href="/lobby/" className="button--medium--outline">Edit Contests</a>
            </div>
          </div>
        </div>
      </div>
    )
  },
})

export default LiveCountdown
