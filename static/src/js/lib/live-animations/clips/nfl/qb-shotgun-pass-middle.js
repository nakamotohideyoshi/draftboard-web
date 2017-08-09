export const clip = {
  frame_width: 180,
  frame_height: 110,
  length: 87,
  registration_x: 178,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 86,
      data: { x: 84, y: 28, in: 86, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 87,
      data: { x: 90, y: 25 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-middle-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-middle-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-middle-white.png'),
  },
};
