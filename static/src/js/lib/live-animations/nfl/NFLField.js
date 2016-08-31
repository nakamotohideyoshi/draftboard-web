import Stage from './Stage';

export default class NFLField extends Stage {

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
    const field = {
      topLeft: { x: 323, y: 80 },
      topRight: { x: 992, y: 80 },
      bottomLeft: { x: 171, y: 243 },
      bottomRight: { x: 1153, y: 243 },
    };

    const fieldTopWidth = field.topRight.x - field.topLeft.x;

    const fieldBottomWidth = field.bottomRight.x - field.bottomLeft.x;

    // Clamp the yardline to avoid going out of bounds.
    const targetYardLine = Math.max(0, Math.min(1, yardLine));

    // flip and clamp the Y offset so the interpolated point's
    // progress is determined top to bottom, with zero being the
    // top of the field and one being the bottom most position.
    const targetOffsetY = 1 - Math.max(0, Math.min(1, offsetY));

    const yardLineTop = {
      x: field.topLeft.x + fieldTopWidth * targetYardLine,
      y: field.topLeft.y,
    };

    const yardLineBottom = {
      x: field.bottomLeft.x + fieldBottomWidth * targetYardLine,
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

    // DEBUG reg point.
    const reg = document.createElement('span');
    reg.className = 'item--reg-point';
    reg.style.top = `${offsetY - 2}px`;
    reg.style.left = `${offsetX - 2}px`;

    const child = this.addChild(node, pos.x, pos.y);
    child.appendChild(reg);

    return child;
  }
}
