import React from 'react'
import PureRenderMixin from 'react-addons-pure-render-mixin';


const LiveStandingsPaneCircle = React.createClass({
  mixins: [PureRenderMixin],

  propTypes: {
    progress: React.PropTypes.number.isRequired
  },

  render() {
    const {progress} = this.props

    let leftStyle = {}
    let rightStyle = {}

    if (progress <= 50) {
      rightStyle.display = 'none'
      leftStyle.transform = `rotate(${Math.round((1 - progress/50)*180)}deg)`
    } else {
      rightStyle.transform = `rotate(${Math.round((1 - (progress - 50)/50)*180)}deg)`
    }

    return (
      <div className="score-circle">
        <div className="circle-right">
          <div className="line" style={rightStyle}></div>
        </div>
        <div className="circle-left">
          <div className="line" style={leftStyle}></div>
        </div>
      </div>
    )
  }
})

export default LiveStandingsPaneCircle
