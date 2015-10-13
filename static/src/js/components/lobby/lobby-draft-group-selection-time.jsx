'use strict';

var React = require('react');
var moment = require('moment');


/**
 * When choosing a draft group, the second step is to pick which time/draft group you want, this
 * renders that list based off of draftGroups from the DraftGroupInfoStore.
 */
var LobbyDraftGroupSelectionTime = React.createClass({

  propTypes: {
    'draftGroups': React.PropTypes.array.isRequired,
    'selectedSport': React.PropTypes.string.isRequired
  },


  getDefaultProps: function() {
    return {
      draftGroups: []
    };
  },


  getDraftGroupUrl: function(draftGroupId) {
    return '/draft/' + draftGroupId + '/';
  },


  render: function() {
    var groups = this.props.draftGroups.map(function(group) {
      if (group.sport === this.props.selectedSport) {
        var url = this.getDraftGroupUrl(group.pk);

        return (
          <li className="cmp-draft-group-select__group" key={group.pk}>
            <a href={url} title="Draft a lineup">
              <h4 className="cmp-draft-group-select__title">
                {moment(group.start).format("dddd, MMM Do - h:mmA")}
              </h4>
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

});


module.exports = LobbyDraftGroupSelectionTime;
