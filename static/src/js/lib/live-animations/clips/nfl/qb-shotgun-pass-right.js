export const clip = {
  frame_width: 140,
  frame_height: 90,
  length: 88,
  registration_x: 134,
  registration_y: 52,
  avatars: [
    {
      name: 'quarterback',
      x: 83,
      y: 13,
      in: 30,
    },
  ],
  data: {
    pass: [20, 20],
  },
  cuepoints: [
    {
      name: 'pass',
      in: 88,
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-white.png'),
  },
};
