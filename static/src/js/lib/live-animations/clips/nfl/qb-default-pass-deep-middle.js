export const clip = {
  frame_width: 210,
  frame_height: 110,
  length: 104,
  registration_x: 188,
  registration_y: 90,
  cuepoints: [
    {
      name: 'avatar',
      in: 30,
      data: { x: 172, y: 36, in: 30, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 104,
      data: { x: 20, y: 20 },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-deep-middle-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-deep-middle-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-deep-middle-white.png'),
    /* eslint-enable max-len*/
  },
};
