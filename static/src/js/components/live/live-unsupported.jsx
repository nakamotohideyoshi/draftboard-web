import React from 'react';

// assets
require('../../../sass/blocks/live/live-unsupported.scss');


/**
 * Stateless component that shows up if you are trying to view live section
 * with unsupported device (currently anything under 1024px)
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const LiveUnsupported = () => {
  const block = 'live-unsupported';

  return (
    <section className={block}>
      <div className={`${block}__inner`}>
        <h2 className={`${block}__title`}>
          The live section requires a minimum width of 1024 pixels.
        </h2>
      </div>
    </section>
  );
};

export default LiveUnsupported;

