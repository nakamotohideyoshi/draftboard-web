import React from 'react'
import {isTimeInFuture} from '../../lib/utils.js'


/**
 * A button for entering contests that will disable itself when the startTime has passed.
 * @param  {[type]}  buttonLabels: A map for button labels.
 */
let EnterContestButton = React.createClass({

  propTypes: {
    startTime: React.PropTypes.string.isRequired,
    isEntered: React.PropTypes.bool.isRequired,
    focusedLineup: React.PropTypes.object,
    contest: React.PropTypes.object.isRequired,
    enterContest: React.PropTypes.func.isRequired,
    buttonLabels: React.PropTypes.object,
    classNames: React.PropTypes.string
  },


  getDefaultProps: function() {
    return {
      buttonLabels: {
        draft: 'Draft',
        enter: 'Enter',
        entered: 'Entered',
        started: 'Contest Started'
      }
    }
  },


  getInitialState: function(){
    return {
      hasContestStarted: false
    }
  },


  ignoreClick: function(e) {
    e.stopPropagation();
  },


  checkStartStatus: function() {
    if (!this.props.contest) {
      return
    }

    this.setState({
      hasContestStarted: !isTimeInFuture(this.props.contest.start)
    })
  },


  componentWillMount: function() {
    // Start a loop that will keep checking if the contest has started yet.
    this.checkStartStatusLoop = window.setInterval(self.checkStartStatus, 1000)
  },


  componentWillUnmount: function() {
    window.clearInterval(this.checkStartStatusLoop)
  },


  render: function() {
    if (this.props.isEntered) {
      return (
        <span
          className={"button button--mini button--green disabled " + this.props.classNames }
          onClick={this.ignoreClick}
        >
          {this.props.buttonLabels.entered}
        </span>
      )
    }

    // If the window to enter the contest has passed, disable the button.
    else if (this.state.hasContestStarted) {
      return (
        <span
          className={"button button--mini--outline button--green-outline " + this.props.classNames}
          onClick={this.ignoreClick}
        >
          {this.props.buttonLabels.started}
        </span>
      )

    }

    // Is the currently focused lineup able to enter this contest?
    else if (this.props.focusedLineup && this.props.focusedLineup.draft_group === this.props.contest.draft_group) {
      return (
        <span
          className={"button button--mini--outline button--green-outline " + this.props.classNames}
          onClick={this.props.enterContest.bind(null, this.props.contest)}
        >
          {this.props.buttonLabels.enter}
        </span>
      )
    }

    // Default to show a draft button.
    else {
      return (
        <a
          className="button button--mini--outline button--green-outline"
          title="Draft a lineup for this contest."
          href={'/draft/' + this.props.contest.draft_group + '/'}
          onClick={this.ignoreClick}
        >
          {this.props.buttonLabels.draft}
        </a>
      )
    }
  }

})


module.exports = EnterContestButton
