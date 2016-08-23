import Stage from './Stage';

export default class NFLField extends Stage {
    
    /**
     * Returns an offset based on the provided side of the field.
     * @param {string}  Side of the field. "left", "middle", "right"
     */
    getSideOffsetY (side = 'middle') {
        let offset = {
            left: .14,
            middle: .41,
            right: .72
        };

        return  offset[side] || offset.middle;
    }

    /**
     * Convert the yardline and Y offset into a x, y coordinate on
     * the field.
     */ 
    getFieldPos (yardLine, offsetY) {
        // Hard coded field dimensions. The field dimensions corespond
        // to the coordinates of the field between endzones.
        let field = {
            topLeft: {x: 323, y: 80},
            topRight: {x: 992, y: 80},
            bottomLeft: {x: 171, y: 243},
            bottomRight: {x: 1153, y: 243}
        };

        const fieldTopWidth = field.topRight.x - field.topLeft.x;

        const fieldBottomWidth = field.bottomRight.x - field.bottomLeft.x;

        // Clamp the yardline to avoid going out of bounds.
        yardLine = Math.max(0, Math.min(1, yardLine));

        // flip and clamp the Y offset so the interpolated point's 
        // progress is determined top to bottom, with zero being the
        // top of the field and one being the bottom most position.
        offsetY = 1 - Math.max(0, Math.min(1, offsetY));

        let yardLineTop = {
            x: field.topLeft.x + fieldTopWidth * yardLine,
            y: field.topLeft.y
        };

        let yardLineBottom = {
            x: field.bottomLeft.x + fieldBottomWidth * yardLine,
            y: field.bottomLeft.y
        };

        let interpolatedPos = {
            x: yardLineBottom.x + (yardLineTop.x - yardLineBottom.x) * offsetY,
            y: yardLineBottom.y + (yardLineTop.y - yardLineBottom.y) * offsetY
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
    addChildAtYardLine (node, yardLine, side = 'middle', offsetX = 0, offsetY = 0) {
        let pos = this.getFieldPos(yardLine, this.getSideOffsetY(side));
        pos.x -= offsetX;
        pos.y -= offsetY;

        //DEBUG reg point.
        let reg = document.createElement('span');
        reg.className = 'item--reg-point';
        reg.style.top = `${offsetY - 2}px`;
        reg.style.left = `${offsetX - 2}px`;

        let child = this.addChild(node, pos.x, pos.y);
        child.appendChild(reg);

        return child;
    }
}
