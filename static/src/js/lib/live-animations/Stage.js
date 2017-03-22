export default class Stage {

  constructor(el) {
    this.el = el;
  }

  /**
   * Returns the full width of field graphic in pixels.
   * @return {number}
   */
  getWidth() {
    return this.el.offsetWidth;
  }

  /**
   * Returns the full height of the field graphic in pixels.
   * @return {number}
   */
  getHeight() {
    return this.el.offsetHeight;
  }

  /**
   * The described coordinates of the stage.
   * @return {Object} topLeft, topRight, bottomLeft and bottomRight.
   */
  getRect() {
    throw new Error('Missing override "getRect()". The method is abstract and should be overwritten.');
  }

  /**
   * Returns the pixel position of the provided x, y percentage.
   * @param {Number} The percent along the x axis.
   * @param {Number} The percent along the y axis.
   * @return {Object} The resulting x, y position in pixels.
   */
  getPosition(percentX, percentY) {
    /**
     * Returns a midpoint between two points based on the
     * provided percentage.
     * @param {Object} Starting x/y coordinate.
     * @param {Object} Ending x/y coordinate.
     * @param {Number} Percent between the start and end.
     * @return {Object} The resulting x/y coordinate.
     */
    const midpoint = (pt1, pt2, p) => ({
      x: pt1.x + (pt2.x - pt1.x) * p,
      y: pt1.y + (pt2.y - pt1.y) * p,
    });

    // TODO: Apply perspective to the coordinate so that a Y
    // coordinate of 0.5 is paced in the visual center of the field.

    const rect = this.getRect();

    const ptA = midpoint(rect.topLeft, rect.bottomLeft, percentY);

    const ptB = midpoint(rect.topRight, rect.bottomRight, percentY);

    const pos = midpoint(ptA, ptB, percentX);

    return pos;
  }

  /**
   * Adds a child node to the field at the specified X and Y
   * coordinates.
   * @param {Node}    Child to add to the field.
   * @param {number}  X position of child.
   * @param {number}  Y position of child.
   */
  addChild(node, x = 0, y = 0, depth = 10) {
    // Wrap the node in a span element for absolutely positioning
    // the element within the field.
    const span = document.createElement('span');
    span.className = 'stage-item';
    span.style.position = 'absolute';
    span.style.left = `${x}px`;
    span.style.top = `${y}px`;
    span.style.zIndex = depth;
    span.appendChild(node);

    this.el.appendChild(span);

    return span;
  }

  /**
   * Removes the specified child from the field.
   */
  removeChild(node) {
    if (node.parentNode && node.parentNode.parentNode === this.el) {
      this.el.removeChild(node.parentNode);
    }
  }

  /**
   * Removes all clips from the field.
   */
  removeAll() {
    while (this.el.hasChildNodes()) {
      this.el.removeChild(this.el.lastChild);
    }
  }
}
