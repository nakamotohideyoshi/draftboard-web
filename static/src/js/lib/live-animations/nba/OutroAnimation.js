import LiveAnimation from '../LiveAnimation';

export default class OutroAnimation extends LiveAnimation {

  play(recap, court) {
    return new Promise((resolve) => {
      court.removeAll();
      resolve();
    });
  }
}
