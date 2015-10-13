'use strict';

var Reflux = require('reflux');
var React = require('react');
var Modal = require('../modal/modal.jsx');
var DraftGroupInfoStore = require('../../stores/draft-group-info-store.js');
var LobbyDraftGroupSelectionSport = require('./lobby-draft-group-selection-sport.jsx');
var LobbyDraftGroupSelectionTime = require('./lobby-draft-group-selection-time.jsx');


/**
 * When in the lobby, to draft a team you first need to select a Draft Group, this creates a Modal
 * to lets the user do that.
 */
var LobbyDraftGroupSelectionModal = React.createClass({

  mixins: [
    Reflux.connect(DraftGroupInfoStore, 'DraftGroupInfo')
  ],


  getInitialState: function() {
    return {
      isOpen: false,
      selectedSport: null,
      DraftGroupInfo: {}
    };
  },


  // Open the modal.
  open: function() {
    this.setState({isOpen: true});
  },


  // This gets called when the user requests to close the modal.
  close: function() {
    // Go back to the first step.
    this.resetSport();
    // close the modal.
    this.setState({isOpen: false});
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
          sportContestCounts={this.state.DraftGroupInfo.sportContestCounts}
          onSportClick={this.selectSport}
        />
      );
    }

    // If a sport HAS been selected, show the upcoming draft groups.
    else {
      return (
        <LobbyDraftGroupSelectionTime
          draftGroups={this.state.DraftGroupInfo.draftGroups}
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
        isOpen={this.state.isOpen}
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
