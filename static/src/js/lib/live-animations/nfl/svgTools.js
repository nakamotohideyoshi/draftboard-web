/**
* Returns an SVG path element.
*/
export function createPath(points) {
  const startX = points[0][0];
  const startY = points[0][1];
  const poly = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  const path = points.reduce(
    (str, pair) => `${str} L${pair[0]} ${pair[1]}`, `M${startX},${startY} `
  );

  poly.setAttribute('d', `${path} Z`);

  return poly;
}

/**
* Returns an SVG element
*/
export function createSVGElement(width, height) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', width); // TODO get field width.
  svg.setAttribute('height', height); // TODO get field height.

  return svg;
}
