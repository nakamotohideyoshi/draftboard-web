export const clip = {
  frame_width: 190,
  frame_height: 110,
  length: 37,
  registration_x: 156,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 30,
      data: { x: 130, y: 32, in: 30, name: 'receiver' },
    },
    {
      name: 'catch',
      in: 31,
      data: { x: 110, y: 10 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-basket-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-basket-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-basket-white.png'),
  },
};
