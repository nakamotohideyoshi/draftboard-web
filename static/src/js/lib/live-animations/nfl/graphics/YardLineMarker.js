import Rectangle from './Rectangle';

export default class YardLineMarker extends Rectangle {
  constructor(field, yardLine, color = '#bdcc1a') {
    // Determine the left and right position of the line based on
    // the width of the line. The width of the line is hardcoded
    // to approximately match the onfield graphics.
    const lineWidth = 0.003;
    const lineLeft = yardLine - lineWidth;

    super(field, lineLeft, 0, lineWidth, 1, color);
  }
}
