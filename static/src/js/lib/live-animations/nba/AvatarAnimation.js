const avatarHTML = require('./avatar.svg');

export default class AvatarAnimation {
  constructor() {
    const width = 95 * 0.5;
    const height = 125 * 0.5;

    this.el = document.createElement('SPAN');

    this.el.style.position = 'absolute';
    this.el.style.left = `-${width * 0.5}px`;
    this.el.style.top = `-${height}px`;

    this.el.style.height = `${height}px`;
    this.el.style.width = `${width}px`;

    this.el.innerHTML = `<img src="${avatarHTML}">`;
  }

  play() {
    // TODO: Animate avatar in.
    return new Promise(resolve => {
      setTimeout(resolve, 2000);
    });
  }

  getElement() {
    return this.el;
  }
}
