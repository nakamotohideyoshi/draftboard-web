import Stage from '../Stage';

export default class NFLField extends Stage {

  /**
   * Returns the pixel coordinates of the retangular field of play.
   * @return {Object}
   */
  getFieldRect() {
    return {
      topLeft: { x: 323, y: 80 },
      topRight: { x: 990, y: 80 },
      bottomLeft: { x: 171, y: 243 },
      bottomRight: { x: 1153, y: 243 },
    };
  }

  /**
   * Stores the current yard line on the field.
   * @param {float}
   */
  setYardLine(value) {
    this._yardline = Math.max(0, Math.min(1, value));
  }

  /**
   * Returns the current yard line on the field. Useful if
   * you have an animation that needs to pick up where the
   * previous one left off.
   */
  getYardLine() {
    return this._yardline || 0;
  }

  /**
   * Converts the given pixel value into yards on the field.
   */
  pixelsToYards(pixels) {
    const field = this.getFieldRect();
    const fieldLength = field.topRight.x - field.topLeft.x;
    const yards = Math.abs(pixels) / (fieldLength / 100);
    return yards / 100;
  }

  /**
   * Returns an offset based on the provided side of the field.
   * @param {string}  Side of the field. "left", "middle", "right"
   */
  getSideOffsetY(side = 'middle') {
    const offset = {
      left: 0.14,
      middle: 0.41,
      right: 0.72,
    };

    return offset[side] || offset.middle;
  }

  /**
   * Convert the yardline and Y offset into a x, y coordinate on
   * the field.
   */
  getFieldPos(yardLine, offsetY) {
    // Hard coded field dimensions. The field dimensions corespond
    // to the coordinates of the field between endzones.
    const field = this.getFieldRect();

    const fieldTopWidth = field.topRight.x - field.topLeft.x;

    const fieldBottomWidth = field.bottomRight.x - field.bottomLeft.x;

    // flip the Y offset so the interpolated point's progress is
    // determined top to bottom, with zero being the top of the field
    // and one being the bottom of the field.
    const targetOffsetY = 1 - offsetY;

    const yardLineTop = {
      x: field.topLeft.x + fieldTopWidth * yardLine,
      y: field.topLeft.y,
    };

    const yardLineBottom = {
      x: field.bottomLeft.x + fieldBottomWidth * yardLine,
      y: field.bottomLeft.y,
    };

    const interpolatedPos = {
      x: yardLineBottom.x + (yardLineTop.x - yardLineBottom.x) * targetOffsetY,
      y: yardLineBottom.y + (yardLineTop.y - yardLineBottom.y) * targetOffsetY,
    };

    return interpolatedPos;
  }

  /**
   * Adds a child node to the field.
   * @param {Node}    Child to add to the field.
   * @param {number}  Yardline position.
   * @param {number}  Which side of the field to place the child.
   * @param {number}  An offset in pixels for the placed child.
   * @param {number}  An offset in pixels for the placed child.
   */
  addChildAtYardLine(node, yardLine, side = 'middle', offsetX = 0, offsetY = 0) {
    const pos = this.getFieldPos(yardLine, this.getSideOffsetY(side));
    pos.x -= offsetX;
    pos.y -= offsetY;

    return this.addChild(node, pos.x, pos.y);
  }
}
