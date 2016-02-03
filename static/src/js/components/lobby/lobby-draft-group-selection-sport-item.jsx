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
    return (
      <li
        className="cmp-draft-group-select__sport"
        onClick={this.handleClick}
      >
        <h4 className="cmp-draft-group-select__title">{this.props.sport}</h4>
        <div className="cmp-draft-group-select__sub">
          {this.props.sportContestCounts[this.props.sport]} contests
        </div>
      </li>
    );
  },

});


module.exports = LobbyDraftGroupSelectionSportItem;
