import React from 'react';


const SkillLevelOverlay = (props) => {
  /**
   * Does the currently selected lineup's sport skill level match the skill level
   * filter that is selected?
   * @return {bool}
   */

  // The sport of the focused lineup.
  let currentSport;
  // The current skill level for that sport.
  let sportSkillLevel;
  let selectedSkillLevel;

  const lineupMatchesFilter = () => {
    if (
        !props.skillLevelFilter ||
        !props.entrySkillLevels ||
        !props.focusedLineup ||
        !props.sportFilter ||
        !props.sportFilter.match
    ) {
      // We don't have enough info to determine if the selected lineup is valid for this skill level.
      return true;
    }

    // The sport of the focused lineup.
    currentSport = props.sportFilter.match; // props.focusedLineup.sport;
    // The current skill level for that sport.
    sportSkillLevel = props.entrySkillLevels[currentSport];
    // The skill level filter that has been selected.
    selectedSkillLevel = props.skillLevelFilter.match[0];

    // We don't have any entries for this sport, don't show the overlay.
    if (typeof(sportSkillLevel) === 'undefined') {
      return true;
    }

    // Does the selected skill level filter match the skill level of the sport?
    return sportSkillLevel === selectedSkillLevel;
  };

  // if they don't match, show a modal blocking entries.
  if (!lineupMatchesFilter()) {
    return (
      <div className="cmp-skill-level-overlay active">
        <div className="modal">
          <div className="content">
            <h3 className="header">{currentSport.toUpperCase()} {selectedSkillLevel} Lobby Locked</h3>
            <p className="body">
              You are currently entered in one or more {currentSport.toUpperCase()} {sportSkillLevel} contests.
              <br />
              To enter {selectedSkillLevel} contests please deregister from all {sportSkillLevel} contests.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="cmp-skill-level-overlay inactive"></div>
  );
};

SkillLevelOverlay.propTypes = {
  // The currently selected skill level (rookie|veteran)
  skillLevelFilter: React.PropTypes.object,
  // A map of all skill levels per-sport.
  entrySkillLevels: React.PropTypes.object,
  // The currently focused lineup.
  focusedLineup: React.PropTypes.object,
  // The currently focused sport object.
  sportFilter: React.PropTypes.object,
};

module.exports = SkillLevelOverlay;
