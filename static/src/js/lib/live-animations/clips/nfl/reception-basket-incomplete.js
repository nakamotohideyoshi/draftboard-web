export const clip = {
  frame_width: 225,
  frame_height: 110,
  length: 46,
  registration_x: 191,
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
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-basket-incomplete-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-basket-incomplete-blue.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-basket-incomplete-blue.png'),
    /* eslint-enable max-len */
  },
};
