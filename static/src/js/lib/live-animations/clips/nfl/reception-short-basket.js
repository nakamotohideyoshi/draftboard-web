export const clip = {
  frame_width: 190,
  frame_height: 110,
  length: 11,
  registration_x: 106,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 10,
      data: { x: 106, y: 32, in: 10, name: 'receiver' },
    },
    {
      name: 'catch',
      in: 11,
      data: { x: 114, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-white.png'),
  },
};
