import LiveAnimation from '../LiveAnimation';
import NBAPlayRecapVO from './NBAPlayRecapVO';
import { getBasketClip } from './getClip';

export default class BasketAnimation extends LiveAnimation {

  play(recap, court) {
    if (!recap.madeShot()) {
      return Promise.resolve();
    }

    const courtPos = court.getRimPos(recap.teamBasket());
    const stagePos = court.getPosition(courtPos.x, courtPos.y);
    const zone = court.getZoneAtPosition(recap.courtPosition(), recap.teamBasket()) + 1;
    const clip = getBasketClip(zone);
    const basketFirstFrame = clip.getCuePoint(recap.whichSide());
    const basketLastFrame = basketFirstFrame + (clip.length - 1);

    if (recap.teamBasket() === NBAPlayRecapVO.BASKET_RIGHT) {
      clip.flip();
    }

    stagePos.x -= clip.offsetX * 0.5;
    stagePos.y -= clip.offsetY * 0.5;

    return clip.load().then(() => {
      court.addChild(clip.getElement(), stagePos.x, stagePos.y);
      return clip.play(basketFirstFrame, basketLastFrame);
    });
  }
}
