export const clip = {
  name: 'qb-default-pass-left',
  frame_width: 190,
  frame_height: 90,
  length: 102,
  registration_x: 158,
  registration_y: 70,
  cuepoints: [
    {
      name: 'avatar',
      in: 84,
      data: { x: 80, y: 20, in: 84, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 90,
      data: { x: 80, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-left-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-left-white.png'),
  },
};
