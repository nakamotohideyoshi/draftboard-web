'use strict';

var Reflux = require('reflux');
var React = require('react');
var Modal = require('../modal/modal.jsx');
var DraftGroupInfoStore = require('../../stores/draft-group-info-store.js');
var moment = require('moment');


/**
 * When in the lobby, to draft a team you first need to select a Draft Group, this creates a Modal
 * to lets the user do that.
 *
 * TODO: once we have a Draft Group API endpoint, make the sport + draft group selections use real
 * data.
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


  getSportCountList: function() {
    if (!this.state.DraftGroupInfo.hasOwnProperty('sportContestCounts')) {
      return (<li>There are no active contests.</li>);
    }

    var sportList = [];

    for (var sport in this.state.DraftGroupInfo.sportContestCounts) {
      if (this.state.DraftGroupInfo.sportContestCounts.hasOwnProperty(sport)) {
        sportList.push(
          <li
            key={sport}
            className="cmp-draft-group-select__sport"
            onClick={this.selectSport.bind(this, sport)}
          >
            <h4 className="cmp-draft-group-select__title">{sport}</h4>
            <div className="cmp-draft-group-select__sub">
              {this.state.DraftGroupInfo.sportContestCounts[sport]} contests
            </div>
          </li>
        );
      }
    }

    return sportList;
  },

  /**
   * Return either a sport or draft group selection panel depending on which step we're on.
   * @return {Object} jsx component.
   */
  getModalContent: function() {
    // If a sport has not been selected yet, show the sports.
    if (this.state.selectedSport === null) {
      var sports = this.getSportCountList();
      return (
        <ul>
          {sports}
        </ul>
      );
    }
    // If a sport HAS been selected, show the upcoming draft groups.
    else {

      var groups = this.state.DraftGroupInfo.draftGroups.map(function(group) {
        if (group.sport === this.state.selectedSport) {
          var url = '/draft/' + group.pk + '/';

          return (
            <li className="cmp-draft-group-select__group" key={group.pk}>
              <a href={url} title="Draft a lineup">
                <h4 className="cmp-draft-group-select__title">{moment(group.start).format("dddd, MMM Do - h:mmA")}</h4>
                <div className="cmp-draft-group-select__sub">
                  {group.contestCount} contests - {group.num_games} games
                </div>
              </a>
            </li>
          );
        }

        return;
      }.bind(this));


      return (
        <div>
          <ul>
            {groups}
          </ul>
        </div>
      );
    }
  },


  render: function() {
    var modalContent = this.getModalContent();
    var title = "Choose a Sport";
    if (this.state.selectedSport) {
      title = "Choose a Start Time";
    }

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
