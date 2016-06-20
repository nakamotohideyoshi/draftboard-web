import throttle from 'lodash/throttle';


/**
 * Lazy load images when they are in the viewport. This has only been tested for use on the draft
 * page.
 */
const LazyLoadImage = (DomSelector) => {
  // This will hold all of our queried dom elements.
  let imageList = [];

  function evaluate() {
    // the bottom of the window viewport.
    const now = window.innerHeight + window.scrollY;

    // Loop through each of our queried images and determine if they should be loaded.
    imageList.forEach((img) => {
      const imageSrc = img.getAttribute('data-src');

      if (!img || !imageSrc) {
        return;
      }

      // Is the image in the viewport?
      if (now >= img.getBoundingClientRect().top && img.getBoundingClientRect().top > 0) {
        // Load the image by moving the data-src to the src attribute.
        img.setAttribute('src', imageSrc);
        img.removeAttribute('data-src');
      }
    });
  }

  // Only let the function run every 250ms. Without this it would run every window.onscroll (a lot).
  const throttledevaluation = throttle(evaluate, 250);


  function reloadImages() {
    // this is janky but it helps to make sure that the image are done being rendered to the DOM.
    setTimeout(() => {
      window.requestAnimationFrame(() => {
        imageList = Array.prototype.slice.call(document.querySelectorAll(`${DomSelector}[data-src]`));
        evaluate();
      });
    }, 0);
  }


  // Add a single, throttled onscroll event listener.
  document.addEventListener('DOMContentLoaded', () => {
    window.onscroll = () => {
      throttledevaluation();
    };
  });


  // Look for images upon instantiation.
  reloadImages();

  // Public methods.
  return {
    evaluate,
    reloadImages,
  };
};


export default LazyLoadImage;
