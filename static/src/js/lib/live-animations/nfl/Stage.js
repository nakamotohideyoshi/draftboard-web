export default class Stage {

    constructor (el) {
        this.el = el;
    }

    /**
     * Returns the full width of field graphic in pixels.
     * @return {number}
     */
    getWidth () {
        return this.el.getBoundingClientRect().width;
    }

    /**
     * Returns the full height of the field graphic in pixels.
     * @return {number}
     */
    getHeight () {
        return this.el.getBoundingClientRect().height;
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
        let span = document.createElement('span');
        span.className = 'field--item'
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
    removeChild (node) {
        if (node.parentNode && node.parentNode.parentNode == this.el) {
            this.el.removeChild(node.parentNode);
        }
    }

    /**
     * Removes all clips from the field.
     */
    removeAll () {
        while (this.el.hasChildNodes()) {
            this.el.removeChild(this.el.lastChild);
        }
    }
}
