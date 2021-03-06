const defaultPlayerSrc = require('../../../../img/blocks/draft-list/lineup-no-player.png');

export default class PlayerAvatar {

  static get HEIGHT() {
    return 129;
  }

  static get WIDTH() {
    return 95;
  }

  static get INTRO_TIME() {
    return 300;
  }

  static get OUTRO_TIME() {
    return 300;
  }

  static get WAIT_TIME() {
    return 2000;
  }

  constructor(playerName, thumbnailURL) {
    this.playerName = playerName;
    this.thumbnailURL = thumbnailURL;

    /* eslint-disable max-len */
    let html = '';
    html += '<svg class="avatar-bg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 95 129">';
    html += '  <path class="avatar-bg__shape" d="M94.8 47.3c0 26.2-47.3 81.7-47.3 81.7S0.2 73.4 0.2 47.3C0.2 21.2 21.3 0 47.5 0S94.8 21.3 94.8 47.3z"/>';
    html += '</svg>';
    html += '<div class="player-headshot">';
    html += '  <div class="player-headshot__container">';
    html += '    <img class="player-headshot__img" alt="Player Headshot" />';
    html += '  </div>';
    html += '</div>';
    html += `<p class="player-name">${this.formatPlayerName(playerName)}</p>`;
    /* eslint-enable max-len */

    this.el = document.createElement('DIV');
    this.el.className = 'avatar--nfl';
    this.el.innerHTML = html;
  }

  getElement() {
    return this.el;
  }

  getWidth() {
    return PlayerAvatar.WIDTH;
  }

  getHeight() {
    return PlayerAvatar.HEIGHT;
  }

  formatPlayerName(name) {
    return name;
  }

  load() {
    return new Promise(resolve => {
      const img = this.el.querySelector('.player-headshot__img');
      img.addEventListener('load', () => resolve());
      img.addEventListener('error', () => {
        img.src = defaultPlayerSrc;
      });
      img.src = this.thumbnailURL;
    });
  }

  play() {
    this.el.classList.add('trans-in');
    return this.wait(PlayerAvatar.INTRO_TIME)
    .then(() => this.wait(PlayerAvatar.WAIT_TIME))
    .then(() => this.el.classList.remove('trans-in'))
    .then(() => this.el.classList.add('trans-out'))
    .then(() => this.wait(PlayerAvatar.OUTRO_TIME))
    .then(() => this.el.classList.remove('trans-out'));
  }

  wait(time) {
    return new Promise(resolve => setTimeout(resolve, time));
  }
}
