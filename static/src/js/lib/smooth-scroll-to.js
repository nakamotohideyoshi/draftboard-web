'use strict';

var EasingFunctions = require('./easing.js');

/**
Example Usage:

  var el = document.querySelector('.container');
  SmoothScrollTo(el, el.scrollTop + 400, 600);
*/


/**
 * Smoothly scroll element to the given target (element.scrollTop) for the given duration.
 * Totally ripped from: https://coderwall.com/p/hujlhg/smooth-scrolling-without-jquery
 *
 * @param  {Object} element The DOM element that is to be scrolled.
 * @param  {int} target     The distance that the target should be scrollTop'd to.
 * @param  {int} duration   The duration of the scroll
 * @param  {Object} easing  An easing function from the easing library.
  */
var SmoothScrollTo = function(element, target, duration, easing) {
    target = Math.round(target);
    duration = Math.round(duration);
    // if no easing function supplied, use this default.
    easing = easing || EasingFunctions.easeInOutQuint;

    if (duration < 0) {
        return Promise.reject("bad duration");
    }
    if (duration === 0) {
        element.scrollTop = target;
        return Promise.resolve();
    }

    var startTime = Date.now();
    var endTime = startTime + duration;

    var startTop = element.scrollTop;
    var distance = target - startTop;

    // based on http://en.wikipedia.org/wiki/Smoothstep
    var smoothStep = function(start, end, point) {
        if(point <= start) { return 0; }
        if(point >= end) { return 1; }
        var x = (point - start) / (end - start); // interpolation

        return easing(x);
    };


    return (function() {
      // This is to keep track of where the element's scrollTop is
      // supposed to be, based on what we're doing
      var previousTop = element.scrollTop;

      // This is like a think function from a game loop
      var scrollFrame = function() {
          if(element.scrollTop !== previousTop) {
              return;
          }

          // set the scrollTop for this frame
          var now = Date.now();
          var point = smoothStep(startTime, endTime, now);
          var frameTop = Math.round(startTop + (distance * point));
          element.scrollTop = frameTop;

          // check if we're done!
          if(now >= endTime) {
              return;
          }

          // If we were supposed to scroll but didn't, then we
          // probably hit the limit, so consider it done; not
          // interrupted.
          if(element.scrollTop === previousTop
              && element.scrollTop !== frameTop) {
              return;
          }
          previousTop = element.scrollTop;

          // schedule next frame for execution
          setTimeout(scrollFrame, 0);
      };

      // boostrap the animation process
      setTimeout(scrollFrame, 0);
    })();
};


module.exports = SmoothScrollTo;
