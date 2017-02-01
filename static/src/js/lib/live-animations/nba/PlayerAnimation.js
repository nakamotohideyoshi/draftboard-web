import AvatarAnimation from './AvatarAnimation';
import NBAPlayRecapVO from './NBAPlayRecapVO';
import LiveAnimation from '../LiveAnimation';
import { getBlockClip, getClip, getJumpshotClip, getStealClip } from './getClip';

export default class PlayerAnimation extends LiveAnimation {

  /**
   * Returns the NBAClip associated with the recap's play type.
   */
  getPlayerClip(recap, court) {
    const zone = court.getZoneAtPosition(recap.courtPosition(), recap.teamBasket()) + 1;

    switch (recap.playType()) {
      case NBAPlayRecapVO.BLOCKED_DUNK:
        return getClip('block_dunk');
      case NBAPlayRecapVO.BLOCKED_LAYUP:
        return getClip('block_layup');
      case NBAPlayRecapVO.BLOCKED_HOOKSHOT:
        return getClip('block_layup');
      case NBAPlayRecapVO.BLOCKED_JUMPSHOT:
        return getBlockClip(zone);
      case NBAPlayRecapVO.DUNK:
        return getClip('dunk');
      case NBAPlayRecapVO.FREETHROW:
        return getClip('freethrow');
      case NBAPlayRecapVO.LAYUP:
        return getClip('layup');
      case NBAPlayRecapVO.HOOKSHOT:
        return getClip('layup');
      case NBAPlayRecapVO.JUMPSHOT:
        return getJumpshotClip(zone);
      case NBAPlayRecapVO.REBOUND:
        return getClip('rebound');
      case NBAPlayRecapVO.STEAL:
        return getStealClip(zone);
      default:
        throw new Error(`Unknown clip for play type "${recap.playType()}"`);
    }
  }

  /**
   * Returns the player's x,y court position in pixels based on
   * the recap's playType.
   */
  getPlayerPosition(recap, court) {
    const teamBasket = recap.teamBasket();
    const playType = recap.playType();

    // Provide static positions for play types that are specific to
    // the animation and not based on the recap's court position.
    const staticPositions = {
      [NBAPlayRecapVO.BLOCKED_DUNK]: { x: 0.075, y: 0.4 },
      [NBAPlayRecapVO.BLOCKED_LAYUP]: { x: 0.075, y: 0.4 },
      [NBAPlayRecapVO.BLOCKED_HOOKSHOT]: { x: 0.075, y: 0.4 },
      [NBAPlayRecapVO.DUNK]: court.getRimPos(teamBasket),
      [NBAPlayRecapVO.FREETHROW]: court.getFreethrowPos(teamBasket),
      [NBAPlayRecapVO.HOOKSHOT]: court.getRimPos(teamBasket),
      [NBAPlayRecapVO.LAYUP]: court.getRimPos(teamBasket),
      [NBAPlayRecapVO.REBOUND]: { x: 0.075, y: 0.4 },
    };

    const pos = staticPositions.hasOwnProperty(playType)
      ? staticPositions[playType]
      : recap.courtPosition();

    // Flip the x coordinate of static positions that were defined only for the
    // left basket.
    if (teamBasket === NBAPlayRecapVO.BASKET_RIGHT) {
      if (playType === NBAPlayRecapVO.REBOUND ||
          playType === NBAPlayRecapVO.BLOCKED_DUNK ||
          playType === NBAPlayRecapVO.BLOCKED_LAYUP ||
          playType === NBAPlayRecapVO.BLOCKED_HOOKSHOT) {
        pos.x = 1 - pos.x;
      }
    }

    return court.getPosition(pos.x, pos.y);
  }

  /**
   * Plays the avatar for a specifc recap, court and clip.
   */
  playAvatarAnimation(recap, court, clip) {
    const avatar = new AvatarAnimation();

    const avatarPos = this.getPlayerPosition(recap, court);
    avatarPos.x -= clip.avatarX * 0.5;
    avatarPos.y -= clip.avatarY * 0.5;
    avatarPos.y -= 30;

    court.addChild(avatar.getElement(), avatarPos.x, avatarPos.y);

    return avatar.play().then(() => {
      court.removeChild(avatar.el);
      return clip;
    });
  }

  play(recap, court) {
    const clip = this.getPlayerClip(recap, court);

    if (recap.teamBasket() === NBAPlayRecapVO.BASKET_RIGHT) {
      clip.flip();
    }

    const pos = this.getPlayerPosition(recap, court);
    pos.x -= clip.offsetX * 0.5;
    pos.y -= clip.offsetY * 0.5;

    return clip.load().then(() => {
      court.addChild(clip.getElement(), pos.x, pos.y);
      return clip.playOnce(clip.getCuePoint(recap.whichSide()));
    });
  }
}
