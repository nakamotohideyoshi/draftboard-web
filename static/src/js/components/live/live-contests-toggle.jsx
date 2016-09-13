import React from 'react';
import * as AppActions from '../../stores/app-state-store';


// assets
require('../../../sass/blocks/live/live-contests-toggle.scss');

/**
 * Action to open contests pane
 */
export default React.createClass({
  viewContestsPane() {
    AppActions.addClass('appstate--live-contests-pane--open');
  },

  render() {
    return (
      <div className="live-contests-toggle" onClick={this.viewContestsPane} />
    );
  },
});
