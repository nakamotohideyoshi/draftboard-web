import React from 'react';
import Modal from '../modal/modal.jsx';
// import CountdownClock from '../site/countdown-clock.jsx';
import Cookies from 'js-cookie';
import classNames from 'classnames';
import EnterContestButton from './enter-contest-button.jsx';
import AppStateStore from '../../stores/app-state-store.js';
import { humanizeCurrency } from '../../lib/utils/currency.js';
// import log from '../../lib/logging';

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
    entrySkillLevels: React.PropTypes.object.isRequired,
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
    AppStateStore.modalOpened();
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
    AppStateStore.modalClosed();
  },


  // When the user clicks the 'enter contest' button.
  handleConfirmEntry() {
    // If they selected the 'don't ask again' button, set a cookie to remember.
    if (!this.state.shouldConfirmEntry) {
      Cookies.set('shouldConfirmEntry', 'false');
    }
    // confirm entry via the provided function.
    this.props.confirmEntry(this.props.contest.id);
    if (Cookies.get(this.props.contest.id) === undefined) {
      Cookies.set(this.props.contest.id, 'false');
    }
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
        showCloseBtn={false}
      >
        <div>
          <div className="cmp-contest-list-confirm-modal">
            <div className="content">
              <div className="content-inner">
                <h3 className="title">{this.props.contest.name}</h3>

                <footer className="footer">
                  <div className="contest-fees footer-section">
                    <span className="footer-title">Prize Pool</span>
                    {humanizeCurrency(this.props.contest.prize_pool)}
                  </div>

                  <div className="contest-fees footer-section">
                    <span className="footer-title">Entries</span>
                    {this.props.contest.current_entries}
                  </div>

                  <div className="contest-countdown footer-section">
                    <span className="footer-title">Fee</span>
                    {humanizeCurrency(this.props.contest.buyin)}
                  </div>
                </footer>
              </div>
              <p>Your first entry is guaranteed to be placed in a contest. Subsequent entries are not guaranteed.
Any entries not placed in contests will be refunded.</p>
              <div className="controls">
                <div
                  className="remember"
                  onClick={this.handleConfirmToggle}
                >
                  <div className={rememberClass}>Don't ask me again</div>
                </div>

                <EnterContestButton
                  lineup={this.props.lineup}
                  contest={this.props.contest}
                  lineupsInfo={this.props.lineupsInfo}
                  onEnterClick={this.handleConfirmEntry}
                  onEnterSuccess={this.close}
                  entrySkillLevels = {this.props.entrySkillLevels}
                  buttonClasses= {{
                    default: 'button--med button--lrg-len button--flat',
                    contestEntered: 'button--med button--lrg-len button--flat',
                    pending: 'button--med button--lrg-len button--flat',
                    contestHasStarted: 'button--med button--lrg-len button--flat',
                  }}
                />
              <div
                className="button button--med button--lrg-len button--outline-alt1 cancel-button"
                onClick={this.close}
              >
                Cancel, don't enter contest
              </div>
              </div>
            </div>
          </div>

        </div>
      </Modal>
    );
  },

});


module.exports = ContestListConfirmModal;
