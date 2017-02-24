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
  getPlayCourtPos(recap, court) {
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

  play(recap, court) {
    const player = this.getPlayerClip(recap, court);
    const avatar = new AvatarAnimation('J. Holter');

    if (recap.teamBasket() === NBAPlayRecapVO.BASKET_RIGHT) {
      player.flip();
    }

    const playerFirstFrame = player.getCuePoint('both'); // recap.whichSide());
    const playerLastFrame = playerFirstFrame + (player.length - 1);
    const playerAvatarIn = playerFirstFrame + player.avatar('player').in;
    const playPos = this.getPlayCourtPos(recap, court);

    // Offset the player's clip by it's offset to make sure it accurately lines
    // up with the play position. The offsetX and offsetY act as a
    // registration point.
    let { x: playerX, y: playerY } = playPos;
    playerX -= player.offsetX * 0.5;
    playerY -= player.offsetY * 0.5;

    // Offset the avatar by its width and height so that the point of the marker
    // is bottom centered to the specified x and y position.
    let { x: avatarX, y: avatarY } = playPos;
    avatarX -= player.avatar('player').offset_x * 0.5 + avatar.getWidth() * 0.5;
    avatarY -= player.avatar('player').offset_y * 0.5 + avatar.getHeight();
    avatarY -= 50; // Force the avatar above the player's head.

    return Promise.all([
      player.load(), avatar.load(recap.player()),
    ])
    .then(() => court.addChild(player.getElement(), playerX, playerY))
    .then(() => player.play(playerFirstFrame, playerAvatarIn))
    .then(() => court.addChild(avatar.getElement(), avatarX, avatarY))
    .then(() => avatar.play())
    .then(() => court.removeChild(avatar.getElement()))
    .then(() => player.play(playerAvatarIn, playerLastFrame));
  }
}
