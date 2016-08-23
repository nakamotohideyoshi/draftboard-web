/**
 * Returns an SVG path element.
 */
export function createPath (points) {
    let startX = points[0][0];
    let startY = points[0][1];
    
    let poly = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    poly.setAttribute('d', points.reduce((str, pair) => {
        return str += `L${pair[0]} ${pair[1]} `;
    }, `M${startX},${startY} `) + 'Z');

    return poly;
}

/**
 * Returns an SVG element
 */
export function createSVGElement (width, height) {
    let svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('width', width); // TODO get field width.
    svg.setAttribute('height', height); // TODO get field height.

    return svg;
}
