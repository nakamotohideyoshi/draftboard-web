export const clip = {
  name: 'qb-shotgun-sack',
  frame_width: 180,
  frame_height: 110,
  length: 67,
  registration_x: 178,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 24,
      data: { x: 113, y: 28, name: 'quarterback' },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-sack-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-sack-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-sack-white.png'),
  },
};
