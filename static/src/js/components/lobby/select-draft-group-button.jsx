import React from 'react';
import find from 'lodash/find';


/**
 * A button that either links to a draft group draft page, or pops up a modal
 * to prompt the user to select a draft group.
 */
const SelectDraftGroupButton = React.createClass({

  propTypes: {
    draftGroupInfo: React.PropTypes.object.isRequired,
    focusedSport: React.PropTypes.string.isRequired,
    onClick: React.PropTypes.func.isRequired,
    style: React.PropTypes.string,
    classNames: React.PropTypes.string,
    title: React.PropTypes.string,
  },


  getDefaultProps() {
    return {
      style: 'button',
      classNames: 'button button--gradient',
    };
  },


  getTitle(title, focusedSport = '') {
    if (title) {
      return title;
    }

    return `New ${focusedSport.toUpperCase()} Lineup`;
  },


  renderButton(draftGroupInfo, focusedSport) {
    // If there is only 1 draft group for this sport, link to it's draft page.
    if (draftGroupInfo.sportDraftGroupCounts[focusedSport] === 1) {
      const draftGroup = find(draftGroupInfo.draftGroups, { sport: focusedSport });

      return (
        <a
          href={`/draft/${draftGroup.pk}`}
          className={this.props.classNames}
        >
          {this.getTitle(this.props.title, focusedSport)} <span className="right">→</span>
        </a>
      );
    }

    // If there are multiple draft groups for this sport, we need to show the
    // selection modal.
    return (
      <span
        onClick={this.props.onClick}
        className={this.props.classNames}
      >
        {this.getTitle(this.props.title, focusedSport)} <span className="right">→</span>
      </span>
    );
  },


  render() {
    return (
      <div className="cmp-select-draft-group-button">
        {this.renderButton(this.props.draftGroupInfo, this.props.focusedSport)}
      </div>
    );
  },

});


module.exports = SelectDraftGroupButton;
