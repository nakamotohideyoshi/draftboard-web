import LiveAnimation from '../LiveAnimation';
import YardLineMarker from './graphics/YardLineMarker';

export default class DownLineAnimation extends LiveAnimation {

  play(recap, field) {
    const marker = new YardLineMarker(field, recap.endingYardLine());
    field.addChild(marker.el, 0, 0, 1);
    return super.play(recap, field);
  }
}
