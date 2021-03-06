import LiveAnimation from '../LiveAnimation';
import NBAPlayRecapVO from './NBAPlayRecapVO';
import { getBasketClip } from './getClip';

export default class BasketAnimation extends LiveAnimation {

  play(recap, court) {
    const zone = court.getZoneAtPosition(recap.courtPosition(), recap.teamBasket()) + 1;

    let clip;

    try {
      clip = getBasketClip(recap.madeShot(), zone);
    } catch (error) {
      return Promise.resolve();
    }

    const courtPos = court.getRimPos(recap.teamBasket());
    const stagePos = court.getPosition(courtPos.x, courtPos.y);

    if (recap.teamBasket() === NBAPlayRecapVO.BASKET_RIGHT) {
      clip.flipH();
    }

    stagePos.x -= clip.offsetX;
    stagePos.y -= clip.offsetY;
    return clip.load().then(() => {
      court.addChild(clip.getElement(), stagePos.x, stagePos.y);
      return clip.play(recap.whichSide());
    });
  }
}
