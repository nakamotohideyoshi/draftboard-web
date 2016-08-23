import React from 'react';


const LobbyDraftGroupSelectionSportItem = React.createClass({

  propTypes: {
    sport: React.PropTypes.string,
    onItemClick: React.PropTypes.func.isRequired,
    sportContestCounts: React.PropTypes.object,
  },


  handleClick() {
    this.props.onItemClick(this.props.sport);
  },


  render() {
    const block = 'cmp-draft-group-select';

    return (
      <li
        className="cmp-draft-group-select__sport"
        onClick={this.handleClick}
      >
        <h4 className="cmp-draft-group-select__title">{this.props.sport}</h4>
        <div className="cmp-draft-group-select__sub">
          {this.props.sportContestCounts[this.props.sport]} contests
        </div>
        <svg className={`${block}__arrow`} viewBox="0 0 39.1 21.79">
          <line className={`${block}__arrow-line`} x1="1.5" y1="10.84" x2="37.6" y2="10.84" />
          <line className={`${block}__arrow-line`} x1="27.49" y1="1.5" x2="37.6" y2="10.84" />
          <line className={`${block}__arrow-line`} x1="27.36" y1="20.29" x2="37.6" y2="10.84" />
        </svg>
      </li>
    );
  },

});


module.exports = LobbyDraftGroupSelectionSportItem;
