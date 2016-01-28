import React from 'react'
import Modal from '../modal/modal.jsx'
import CountdownClock from '../site/countdown-clock.jsx'
import Cookies from 'js-cookie'
import ClassNames from 'classnames'
import {find as _find} from 'lodash'


/**
 * When a user attempts to enter a contest, prompt them to confirm.
 */
var ContestListConfirmModal = React.createClass({

  propTypes: {
    lineupId: React.PropTypes.number,
    contest: React.PropTypes.object,
    confirmEntry: React.PropTypes.func.isRequired,
    cancelEntry: React.PropTypes.func.isRequired,
    isOpen: React.PropTypes.bool,
    entryRequests: React.PropTypes.object
  },


  getInitialState: function() {
    return {
      isOpen: this.props.isOpen,
      shouldConfirmEntry: true
    };
  },


  // Open the modal.
  open: function() {
    this.setState({isOpen: true});
  },


  // If the parent component tells us the modal should be closed via prop change, close it.
  // The parent can also call this components 'close()' method directly.
  componentWillReceiveProps: function(nextProps) {
    this.setState({isOpen: nextProps.isOpen})
  },


  // This gets called when the user requests to close the modal.
  close: function() {
    // close the modal.
    this.setState({isOpen: false});
    this.props.cancelEntry()
  },


  // When the user clicks the 'enter contest' button.
  handleConfirmEntry: function() {
    // If they selected the 'don't ask again' button, set a cookie to remember.
    if (!this.state.shouldConfirmEntry) {
      Cookies.set('shouldConfirmEntry', 'false')
    }
    // confirm entry via the provided function.
    this.props.confirmEntry(this.props.contest.id)
    // this.setState({isOpen: false});
  },


  renderCurrentEntryRequestStatus: function() {
    let currentEntryStatus = _find(this.props.entryRequests, {
      lineupId: this.props.lineupId, contestId: this.props.contest.id
    })

    if (currentEntryStatus) {
      return (
        <div>
          {currentEntryStatus.status}
        </div>
      )
    } else {
      return (
        <div>no status</div>
      )
    }

  },


  // Toggle the "don't ask again" button
  handleConfirmToggle: function() {
    this.setState({shouldConfirmEntry: !this.state.shouldConfirmEntry})
  },


  render: function() {
    if (!this.props.contest) {
      return (<div></div>)
    }

    let rememberClass = ClassNames('remember__inner', {'selected': !this.state.shouldConfirmEntry})

    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className="cmp-modal--contest-list-confirm"
      >
        <div>
          <header className="cmp-modal__header">Confirm Entry</header>

          <div className="cmp-contest-list-confirm-modal">
            <div className="content">
              <div className="content-inner">
                <h3 className="title">{this.props.contest.name}</h3>

                <footer className="footer">
                  <div className="contest-fees footer-section">
                    <span className="footer-title">Fees</span>
                    ${this.props.contest.buyin}
                  </div>

                  <div className="contest-countdown footer-section">
                    <span className="footer-title">Live In</span>
                    <CountdownClock time={this.props.contest.start} />
                  </div>
                </footer>
              </div>

              <div className="controls">
                <div
                  className="remember"
                  onClick={this.handleConfirmToggle}
                >
                  <div className={rememberClass}>Don't ask me again.</div>
                </div>

                <div
                  className="button button--large button--gradient--background"
                  onClick={this.handleConfirmEntry}
                >
                  Enter Contest
                </div>
                {this.renderCurrentEntryRequestStatus()}
              </div>
            </div>
          </div>

        </div>
      </Modal>
    );
  }

});

module.exports = ContestListConfirmModal;
