import React from 'react';
import Modal from '../modal/modal.jsx';
import CountdownClock from '../site/countdown-clock.jsx';
import Cookies from 'js-cookie';
import classNames from 'classnames';
import EnterContestButton from './enter-contest-button.jsx';


/**
 * When a user attempts to enter a contest, prompt them to confirm.
 */
const ContestListConfirmModal = React.createClass({

  propTypes: {
    lineup: React.PropTypes.object,
    contest: React.PropTypes.object,
    confirmEntry: React.PropTypes.func.isRequired,
    cancelEntry: React.PropTypes.func.isRequired,
    isOpen: React.PropTypes.bool,
    entries: React.PropTypes.object,
    lineupsInfo: React.PropTypes.object,
  },


  getInitialState() {
    return {
      isOpen: this.props.isOpen,
      shouldConfirmEntry: true,
    };
  },


  // If the parent component tells us the modal should be closed via prop change, close it.
  // The parent can also call this components 'close()' method directly.
  componentWillReceiveProps(nextProps) {
    this.setState({ isOpen: nextProps.isOpen });
  },


  // Open the modal.
  open() {
    this.setState({ isOpen: true });
  },


  // This gets called when the user requests to close the modal.
  close() {
    // close the modal.
    this.setState({ isOpen: false });
    this.props.cancelEntry();
  },


  // When the user clicks the 'enter contest' button.
  handleConfirmEntry() {
    // If they selected the 'don't ask again' button, set a cookie to remember.
    if (!this.state.shouldConfirmEntry) {
      Cookies.set('shouldConfirmEntry', 'false');
    }
    // confirm entry via the provided function.
    this.props.confirmEntry(this.props.contest.id);
    this.close();
  },


  // Toggle the "don't ask again" button
  handleConfirmToggle() {
    this.setState({ shouldConfirmEntry: !this.state.shouldConfirmEntry });
  },


  render() {
    if (!this.props.contest) {
      return (<div></div>);
    }

    const rememberClass = classNames('remember__inner', { selected: !this.state.shouldConfirmEntry });

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
                <EnterContestButton
                  lineup={this.props.lineup}
                  contest={this.props.contest}
                  lineupsInfo={this.props.lineupsInfo}
                  onEnterClick={this.handleConfirmEntry}
                  onEnterSuccess={this.close}
                  buttonClasses= {{
                    default: 'button--med button--lrg-len button--flat',
                    contestEntered: 'button--med button--lrg-len button--flat',
                    pending: 'button--med button--lrg-len button--flat',
                    contestHasStarted: 'button--med button--lrg-len button--flat',
                  }}
                />
              </div>
            </div>
          </div>

        </div>
      </Modal>
    );
  },

});


module.exports = ContestListConfirmModal;
