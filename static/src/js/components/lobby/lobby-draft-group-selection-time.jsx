import React from 'react';
import moment from 'moment';
import { map as _map } from 'lodash';


/**
 * When choosing a draft group, the second step is to pick which time/draft group you want, this
 * renders that list based off of draftGroups from the DraftGroupInfoStore.
 */
const LobbyDraftGroupSelectionTime = React.createClass({

  propTypes: {
    draftGroups: React.PropTypes.object.isRequired,
    selectedSport: React.PropTypes.string.isRequired,
  },


  getDefaultProps() {
    return {
      draftGroups: {},
    };
  },


  getDraftGroupUrl(draftGroupId) {
    return `/draft/${draftGroupId}/`;
  },


  render() {
    const self = this;

    const groups = _map(self.props.draftGroups, (group) => {
      if (group.sport === self.props.selectedSport) {
        const url = self.getDraftGroupUrl(group.pk);

        return (
          <li className="cmp-draft-group-select__group" key={group.pk}>
            <a href={url} title="Draft a lineup">
              <h4 className="cmp-draft-group-select__title">
                {moment(group.start).format('dddd, MMM Do - h:mmA')}
              </h4>
              <div className="cmp-draft-group-select__sub">
                {group.contestCount} contests - {group.num_games} games
              </div>
            </a>
          </li>
        );
      }

      return '';
    });


    return (
      <div>
        <ul>
          {groups}
        </ul>
      </div>
    );
  },

});


module.exports = LobbyDraftGroupSelectionTime;
