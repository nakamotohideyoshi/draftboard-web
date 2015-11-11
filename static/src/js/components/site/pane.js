var KeypressActions = require('../../actions/keypress-actions')
import * as AppActions from '../../stores/app-state-store.js'


/**
 * The full-window side pane slideout thing.
 */
var Pane = (function() {
  // The Escape button should close the pane.
  KeypressActions.keypressESC.listen(AppActions.closePane);

  // Close the pane when the background is clicked.
  var bgCover = document.querySelector('.pane__bg-cover');
  var closeBtn = document.querySelector('.pane__close');

  if (closeBtn) {
    closeBtn.addEventListener('click', function() {
      AppActions.closePane();
    });
  }

  if (bgCover) {
    bgCover.addEventListener('click', function() {
      AppActions.closePane();
    });
  }

})()


module.exports = Pane
