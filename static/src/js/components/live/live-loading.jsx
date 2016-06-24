import React from 'react';

// assets
require('../../../sass/blocks/live/live-loading.scss');


/**
 * Loading screen for live section
 */
const LiveLoading = (props) => {
  const block = 'live-loading';

  let contestPoolsDom = '';
  if (props.isContestPools) {
    contestPoolsDom = (<div className={`${block}__contest-pools`}>Generating contest pools</div>);
  }

  return (
    <div className={block}>
      <div className={`${block}__preload-court`} />
      <div className={`${block}__spinner`}>
        {contestPoolsDom}
        <div className={`${block}__double-bounce1`} />
        <div className={`${block}__double-bounce2`} />
      </div>
    </div>
  );
};

LiveLoading.propTypes = {
  isContestPools: React.PropTypes.bool.isRequired,
};

export default LiveLoading;
