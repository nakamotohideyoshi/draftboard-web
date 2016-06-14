import React from 'react';


/**
 * Loading screen for live section
 */
const LiveLoading = (props) => {
  let contestPoolsDom = '';
  if (props.isContestPools) {
    contestPoolsDom = (<div className="live--loading__pools">Generating contest pools</div>);
  }

  return (
    <div className="live__bg">
      <div className="live--loading">
        <div className="preload-court" />
        <div className="spinner">
          {contestPoolsDom}
          <div className="double-bounce1" />
          <div className="double-bounce2" />
        </div>
      </div>
    </div>
  );
};

LiveLoading.propTypes = {
  isContestPools: React.PropTypes.bool.isRequired,
};

export default LiveLoading;
