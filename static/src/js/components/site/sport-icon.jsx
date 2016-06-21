import React from 'react';


/**
 * Tiny sport ball icons seen on the contest list or lineup card title.
 */
const SportIcon = (props) => <div className={`cmp-sport-icon icon-${props.sport}`}></div>;

SportIcon.propTypes = {
  sport: React.PropTypes.string.isRequired,
};


module.exports = SportIcon;
