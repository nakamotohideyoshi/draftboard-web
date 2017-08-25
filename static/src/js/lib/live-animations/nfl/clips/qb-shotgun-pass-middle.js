export const clip = {
  name: 'qb-shotgun-pass-middle',
  frame_width: 180,
  frame_height: 110,
  length: 87,
  registration_x: 178,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 61,
      data: { x: 48, y: 28, type: 'quarterback' },
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
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-middle-white.png'),
  },
};
