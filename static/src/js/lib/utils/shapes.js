/**
 * Convert polar coordinates into cartesian
 * - Polar coordinates are when you have an origin x,y coordinate, a radius, and an angle
 * - Cartesian coordinates are where you have an origin x,y coordinate, and then x and y distances to go to
 *
 * Method based on http://goo.gl/yJFZMs
 *
 * @param  {number} The origin x coordinate
 * @param  {number} The origin y coordinate
 * @param  {number} Radius from the origin point
 * @param  {number} Angle of the line created of distance radius from the origin x,y
 * @return {object} Object with x and y distances to go from origin x,y coordinate
 */
export const polarToCartesian = (originX, originY, radius, angleInDegrees) => {
  const modAngle = angleInDegrees % 360;
  const angleInRadians = (modAngle - 90) / 180 * Math.PI;

  return {
    x: Math.round(originX + (radius * Math.cos(angleInRadians)) * 1E7) / 1E7,
    y: Math.round(originY + (radius * Math.sin(angleInRadians)) * 1E7) / 1E7,
  };
};

/**
 * Generate svg arc path, based on method from http://goo.gl/yJFZMs
 * - limited to positive arc between 0 and 360, represents 0 to 100% for us
 *
 * @param  {number} Origin x coordinate
 * @param  {number} Origin y coordinate
 * @param  {number} Radius to go from origin x,y
 * @param  {number} Starting angle (limited 0 to 360)
 * @param  {number} Ending angle (limited 0 to 360)
 * @return {string} Generated arc path used in an svg
 */
export const describeArc = (x, y, radius, startAngle, endAngle) => {
  const limitedStartAngle = Math.min(Math.max(startAngle, 0), 360);
  const limitedEndAngle = Math.min(Math.max(endAngle, 0), 360);

  // determine start and end cartesian paths
  const start = polarToCartesian(x, y, radius, limitedEndAngle);
  const end = polarToCartesian(x, y, radius, limitedStartAngle);

  // determine the semicircle on which the arc goes, 0 being left 1 being right
  const arcSweep = limitedEndAngle - limitedStartAngle <= 180 ? '0' : '1';

  return [
    'M', start.x, start.y,
    'A', radius, radius, 0, arcSweep, 0, end.x, end.y,
  ].join(' ');
};
