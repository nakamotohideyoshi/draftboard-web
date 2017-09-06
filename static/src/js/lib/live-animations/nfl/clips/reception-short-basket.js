export const clip = {
  name: 'reception-short-basket',
  frame_width: 190,
  frame_height: 110,
  length: 11,
  registration_x: 106,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 10,
      data: { x: 106, y: 32, type: 'receiver' },
    },
    {
      name: 'catch',
      in: 11,
      data: { x: 106, y: 32 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-white.png'),
  },
};
