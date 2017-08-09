export const clip = {
  frame_width: 150,
  frame_height: 90,
  length: 94,
  registration_x: 120,
  registration_y: 60,
  avatars: [
    {
      name: 'quarterback',
      x: 107,
      y: 20,
      in: 30,
    },
  ],
  data: {
    pass: [0, 0],
  },
  cuepoints: [
    {
      name: 'pass',
      in: 94,
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-right-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-right-white.png'),
  },
};
