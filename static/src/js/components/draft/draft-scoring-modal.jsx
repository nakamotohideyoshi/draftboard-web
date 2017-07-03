import React from 'react';
import Modal from '../modal/modal.jsx';
import AppStateStore from '../../stores/app-state-store.js';


/**
 * When a user attempts to enter a contest, prompt them to confirm.
 */
const DraftScoringModal = React.createClass({

  propTypes: {
    onClose: React.PropTypes.func.isRequired,
    isOpen: React.PropTypes.bool,
    children: React.PropTypes.element.isRequired,
    sport: React.PropTypes.string.isRequired,
  },


  getInitialState() {
    return {
      isOpen: this.props.isOpen,
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
    AppStateStore.modalClosed();
  },


  // When the user clicks the 'cancel' button.
  handleOnClose(event) {
    if (event) event.preventDefault();
    // confirm entry via the provided function.
    this.props.onClose();
    this.close();
  },


  render() {
    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.handleOnClose}
        className="cmp-modal--draft-scoring"
      >
        <div>
          <div className="cmp-draft-scoring-modal">
            <div className="content">
              <div className="closeButton" />

              <div className="content-inner">
                <div className="title">{this.props.sport} SCORING</div>
                <div className="text-content">{this.props.children}</div>
              </div>

              <div className="controls">
                <div
                  className="button button--gradient button--med ok-button"
                  onClick={this.handleOnClose}
                >
                  GO IT
                </div>
              </div>
            </div>
          </div>

        </div>
      </Modal>
    );
  },

});


module.exports = DraftScoringModal;
