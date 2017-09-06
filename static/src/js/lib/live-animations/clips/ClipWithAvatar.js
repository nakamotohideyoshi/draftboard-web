import Clip from './Clip';
import PlayerAvatar from './PlayerAvatar';

export default class ClipWithAvatar {

  static get AVATAR_Y_OFFSET() {
    return 10;
  }

  constructor(clipData) {
    this._data = clipData;
    this._clip = new Clip(this._data);
    this._avatars = [];
  }

  setPlayers(players, sport) {
    // Create a collection of PlayerAvatars based on the provided recap
    // and clip. Only player types defined in both the clip and recap result in
    // the creation of a PlayerAvatar.
    this._avatars = players.filter(player =>
      this.getCuepointForAvatar(player.avatarType) !== null
    ).map(player => {
      const playerName = `${player.first_name} ${player.last_name}`;
      const playerThumb = `${window.dfs.playerImagesBaseUrl}/${sport}/120/${player.srid_player}.png`;
      const avCuepoint = this.getCuepointForAvatar(player.avatarType);
      const avData = avCuepoint.data;
      const avAnimation = new PlayerAvatar(playerName, playerThumb);
      const avAnimationEl = avAnimation.getElement();
      const avWidth = avAnimation.getWidth();
      const avatarY = avData.y * 0.5 - avAnimation.getHeight() - ClipWithAvatar.AVATAR_Y_OFFSET;

      let avatarX = avData.x * 0.5 - avWidth * 0.5;

      // TODO: handle flipped clips.
      if (this._clip.isFlipped()) {
        avatarX = this._clip.screenWidth - avData.x * 0.5 - avWidth * 0.5;
      }

      avAnimationEl.style.position = 'absolute';
      avAnimationEl.style.top = `${avatarY}px`;
      avAnimationEl.style.left = `${avatarX}px`;

      return {
        name: avData.type,
        in: avCuepoint.in,
        x: avData.x,
        y: avData.y,
        animation: avAnimation,
        data: avCuepoint.data,
      };
    }).sort(
      (a, b) => a.in - b.in // Chronologically
    );
  }

  debug() {
    this._clip.debug();
  }

  flipH() {
    this._clip.flipH();
  }

  get clip() {
    return this._clip;
  }
  get offsetX() {
    return this._clip.registrationX;
  }

  get offsetY() {
    return this._clip.registrationY;
  }

  getElement() {
    return this._clip.getElement();
  }

  /**
   * Returns the cuepoint associated with the provided avatar.
   */
  getCuepointForAvatar(type) {
    return this._data.cuepoints.find(cuepoint => cuepoint.data.type === type) || null;
  }

  /**
   * Loads the clip with avatars for the provided list of players.
   */
  load(players, sport) {
    const playersWithAvatars = players.filter(player => (
      this.getCuepointForAvatar(player.avatarType) !== null
    ));

    this.setPlayers(playersWithAvatars, sport);

    const color = playersWithAvatars.reduce((lineup, player) => (
      lineup === null ? player.lineup : lineup
    ), null);

    return Promise.all([
      this._clip.load(color || 'none'),
      Promise.all(this._avatars.map(avatar => avatar.animation.load())),
    ]).then(() => this);
  }

  /**
   * ...
   */
  playAvatar(avatarName) {
    const avatar = this._avatars.find(avatarData =>
      avatarData.name === avatarName
    );

    if (!avatar) {
      return Promise.resolve();
    }

    const avatarEl = avatar.animation.getElement();
    this._clip.getElement().appendChild(avatarEl);

    return avatar.animation.play().then(() => {
      this._clip.getElement().removeChild(avatarEl);
      return avatar;
    });
  }

  /**
   * ...
   */
  goto(frame) {
    this._clip.goto(frame);
  }
}
