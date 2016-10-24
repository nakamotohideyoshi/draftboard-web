import React from 'react';


const ProbablePitchersFilter = React.createClass({
  propTypes: {
    enabled: React.PropTypes.bool,
    onUpdate: React.PropTypes.func.isRequired,
    sport: React.PropTypes.string,
  },


  getDefaultProps() {
    return {
      enabled: true,
      sport: null,
    };
  },

  handleClick() {
    // Toggle the enabled/disabled match state.
    this.props.onUpdate('probablePitchersFilter', 'srid', !this.props.enabled);
  },


  render() {
    // Don't show for anything other than MLB.
    if (this.props.sport !== 'mlb') {
      return <div className="cmp-probable-pitchers-filter disabled"></div>;
    }

    return (
      <div className="cmp-probable-pitchers-filter">
        <div className="radio-button-list__button-container">
          <input
            className="radio-button-list__input"
            type="radio"
            id="inputProbablyPitchers"
            name="inputProbablyPitchers"
            onChange={() => true}
            checked={this.props.enabled}
          />
          <label
            className="radio-button-list__label"
            htmlFor="inputProbablyPitchers"
            onClick={this.handleClick}
          ></label>
        <span className="text_label" onClick={this.handleClick}>Probable Pitchers Only</span>
        </div>
      </div>
    );
  },
});


module.exports = ProbablePitchersFilter;
