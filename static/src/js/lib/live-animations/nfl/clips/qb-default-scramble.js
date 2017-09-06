export const clip = {
  name: 'qb-default-scramble',
  frame_width: 170,
  frame_height: 80,
  length: 103,
  registration_x: 144,
  registration_y: 56,
  cuepoints: [
    {
      name: 'avatar',
      in: 30,
      data: { x: 50, y: 0, type: 'receiver', pause: true },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-scramble-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-scramble-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-scramble-red.png'),
  },
};
