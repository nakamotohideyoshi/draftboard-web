export const clip = {
  name: 'qb-default-pass-deep-middle',
  frame_width: 210,
  frame_height: 110,
  length: 104,
  registration_x: 188,
  registration_y: 90,
  cuepoints: [
    {
      name: 'avatar',
      in: 65,
      data: { x: 48, y: 32, type: 'quarterback', pause: true },
    },
    {
      name: 'pass',
      in: 90,
      data: { x: 90, y: 20 },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-deep-middle-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-deep-middle-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-deep-middle-white.png'),
    /* eslint-enable max-len*/
  },
};
