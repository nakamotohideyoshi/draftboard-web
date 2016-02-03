// import KeypressActions from '../../actions/keypress-actions';
import * as AppActions from '../../stores/app-state-store.js';


/**
 * The full-window side pane slideout thing.
 */
const Pane = () => {
  // The Escape button should close the pane.
  // KeypressActions.keypressESC.listen(AppActions.closePane);

  // Close the pane when the background is clicked.
  const bgCover = document.querySelector('.pane__bg-cover');
  const closeBtn = document.querySelector('.pane__close');

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      AppActions.closePane();
    });
  }

  if (bgCover) {
    bgCover.addEventListener('click', () => {
      AppActions.closePane();
    });
  }
};


module.exports = Pane;
