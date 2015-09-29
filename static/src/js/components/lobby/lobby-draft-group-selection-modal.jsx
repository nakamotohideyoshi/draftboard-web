'use strict';

var React = require('react');
var Modal = require('../modal/modal.jsx');


/**
 * When in the lobby, to draft a team you first need to select a Draft Group, this creates a Modal
 * to lets the user do that.
 *
 * TODO: once we have a Draft Group API endpoint, make the sport + draft group selections use real
 * data.
 */
var LobbyDraftGroupSelectionModal = React.createClass({

  getInitialState: function() {
    return {
      isOpen: false,
      selectedSport: null
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
        <ul>
          <li className="cmp-draft-group-select__sport" onClick={this.selectSport.bind(this, 'nba')}>NBA</li>
          <li className="cmp-draft-group-select__sport" onClick={this.selectSport.bind(this, 'mlb')}>MLB</li>
          <li className="cmp-draft-group-select__sport" onClick={this.selectSport.bind(this, 'nfl')}>NFL</li>
        </ul>
      );
    }
    // If a sport HAS been selected, show the upcoming draft groups.
    else {
      return (
        <div>
          <h3
            className="cmp-draft-group-select__selected-sport"
            onClick={this.resetSport}
          >
            <span>{this.state.selectedSport}</span>
          </h3>

          <ul>
            <li className="cmp-draft-group-select__group">
              <a href="/draft/1/" title="Draft a lineup">
                <span className="cmp-draft-group-select__title">Today</span>
                <span className="cmp-draft-group-select__date">18</span>
                <span className="cmp-draft-group-select__time">1:20PM</span>
              </a>
            </li>
            <li className="cmp-draft-group-select__group">
              <a href="/draft/1/" title="Draft a lineup">
                <span className="cmp-draft-group-select__title">Today</span>
                <span className="cmp-draft-group-select__date">18</span>
                <span className="cmp-draft-group-select__time">5:00PM</span>
              </a>
            </li>
          </ul>
        </div>
      );
    }
  },


  render: function() {
    var modalContent = this.getModalContent();
    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
      >
        <div>
          <header className="cmp-modal__header">Choose a Sport &amp; Time</header>

          <div className="cmp-draft-group-select">
            {modalContent}
          </div>
        </div>
      </Modal>
    );
  }

});

module.exports = LobbyDraftGroupSelectionModal;
