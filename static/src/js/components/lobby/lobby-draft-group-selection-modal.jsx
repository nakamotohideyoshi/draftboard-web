var React = require('react');
var Modal = require('../modal/modal.jsx');
var LobbyDraftGroupSelectionSport = require('./lobby-draft-group-selection-sport.jsx');
var LobbyDraftGroupSelectionTime = require('./lobby-draft-group-selection-time.jsx');


/**
 * When in the lobby, to draft a team you first need to select a Draft Group, this creates a Modal
 * to lets the user do that.
 */
var LobbyDraftGroupSelectionModal = React.createClass({

  propTypes: {
    draftGroupInfo: React.PropTypes.object,
    isOpen: React.PropTypes.bool,
    onClose: React.PropTypes.func
  },


  getInitialState: function() {
    return {
      selectedSport: null
    };
  },


  // Open the modal.
  // open: function() {
  //   this.setState({isOpen: true});
  // },


  // This gets called when the user requests to close the modal.
  close: function() {
    // Run the props-passed onClose function that hides the modal.
    this.props.onClose()
    // Go back to the first step.
    this.resetSport();
  },


  // Reset the sport selection.
  resetSport: function() {
    this.setState({selectedSport: null});
  },


  // Select a sport.
  selectSport: function(sport) {
    this.setState({selectedSport: sport});
  },


  /**
   * Return either a sport or draft group selection panel depending on which step we're on.
   * @return {Object} jsx component.
   */
  getModalContent: function() {
    // If a sport has not been selected yet, show the sports.
    if (this.state.selectedSport === null) {
      return (
        <LobbyDraftGroupSelectionSport
          sportContestCounts={this.props.draftGroupInfo.sportContestCounts}
          onSportClick={this.selectSport}
        />
      );
    }

    // If a sport HAS been selected, show the upcoming draft groups.
    else {
      return (
        <LobbyDraftGroupSelectionTime
          draftGroups={this.props.draftGroupInfo.draftGroups}
          selectedSport={this.state.selectedSport}
        />
      );
    }
  },


  render: function() {
    var modalContent = this.getModalContent();
    var title = (this.state.selectedSport) ? "Choose a Start Time" : "Choose a Sport";

    return (
      <Modal
        isOpen={this.props.isOpen}
        onClose={this.close}
        className="cmp-modal--draft-group-select"
      >
        <div>
          <header className="cmp-modal__header">{title}</header>

          <div className="cmp-draft-group-select">
            {modalContent}
          </div>
        </div>
      </Modal>
    );
  }

});

module.exports = LobbyDraftGroupSelectionModal;
