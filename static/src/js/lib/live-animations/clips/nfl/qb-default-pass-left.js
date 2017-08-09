export const clip = {
  frame_width: 190,
  frame_height: 90,
  length: 102,
  registration_x: 158,
  registration_y: 70,
  cuepoints: [
    {
      name: 'avatar',
      in: 101,
      data: { x: 141, y: 20, in: 101, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 102,
      data: { x: 20, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-left-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-left-white.png'),
  },
};
