import React from 'react';
import moment from 'moment';
import map from 'lodash/map';


/**
 * When choosing a draft group, the second step is to pick which time/draft group you want, this
 * renders that list based off of draftGroups from the DraftGroupInfoStore.
 */
const LobbyDraftGroupSelectionTime = React.createClass({

  propTypes: {
    draftGroups: React.PropTypes.array.isRequired,
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
    const block = 'cmp-draft-group-select';

    const groups = map(self.props.draftGroups, (group) => {
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
            <svg className={`${block}__arrow`} viewBox="0 0 39.1 21.79">
              <line className={`${block}__arrow-line`} x1="1.5" y1="10.84" x2="37.6" y2="10.84" />
              <line className={`${block}__arrow-line`} x1="27.49" y1="1.5" x2="37.6" y2="10.84" />
              <line className={`${block}__arrow-line`} x1="27.36" y1="20.29" x2="37.6" y2="10.84" />
            </svg>
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
