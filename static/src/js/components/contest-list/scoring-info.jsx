import React from 'react';

// Map of player action -> fantasy points awarded
const events = {
  nba: [
    { title: 'Point', value: '1 pt' },
    { title: 'Assist', value: '1.5 pts' },
    { title: 'Rebound', value: '1.25 pts' },
    { title: 'Steal', value: '2 pts' },
    { title: 'Block', value: '2 pts' },
    { title: 'Turnover', value: '-0.5 pts' },
  ],
  nfl: [
    { title: 'Passing Yard', value: '0.04 pts' },
    { title: 'Passing TD', value: '4 pts' },
    { title: 'Interception', value: '-1 pts' },
    { title: 'Reception', value: '0.5 pts' },
    { title: 'Receiving Yard', value: '0.1 pts' },
    { title: 'Receiving TD', value: '6 pts' },
    { title: 'Rushing Yard', value: '0.1 pts' },
    { title: 'Rushing TD', value: '6 pts' },
    { title: '2 Point Conversion', value: '2 pts' },
    { title: 'Fumble', value: '-0.1 pts' },
  ],
  nhl: [],
  mlb: [{
    hitter: [
      { title: 'Stolen Base', value: '6 pts' },
      { title: 'RBI', value: '2 pts' },
      { title: 'Single', value: '3 pts' },
      { title: 'Double', value: '6 pts' },
      { title: 'Triple', value: '9 pts' },
      { title: 'Home Run', value: '12 pts' },
      { title: 'RBI', value: '2 pts' },
      { title: 'Walk ', value: '3 pts' },
      { title: 'Hit By Pitch', value: '3 pts' },
    ],
    pitcher: [
      { title: 'Strike Out', value: '3 pts' },
      { title: 'Walk', value: '-1 pts' },
      { title: 'Hit Batter', value: '-1 pts' },
      { title: 'Earned Run', value: '-3 pts' },
    ],
  }],
};


/**
 * Render a list of <tr> elements for supplied events.
 */
const renderEvents = (sport) => {
  if (sport in events) {
    return events[sport].map((event, i) => (
      <tr key={i}>
      <td>{event.title}</td>
      <td>{event.value}</td>
      </tr>
    ));
  }
};


/**
 * Print out a table of fantasy points awarded for each type of player action.
 */
const ScoringInfo = (props) => (
  <div className="cmp-scoring-info">
    <table className="table">
      <thead>
        <tr>
          <th className="title">Event</th>
          <th className="title">Points</th>
        </tr>
      </thead>
      <tbody>
        {renderEvents(props.sport)}
      </tbody>
    </table>
  </div>
);


ScoringInfo.propTypes = {
  sport: React.PropTypes.string.isRequired,
};


module.exports = ScoringInfo;
