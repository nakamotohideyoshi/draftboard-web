export const clip = {
  name: 'reception-short-basket-incomplete',
  frame_width: 225,
  frame_height: 100,
  length: 25,
  registration_x: 106,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 10,
      data: { x: 106, y: 22, type: 'receiver' },
    },
    {
      name: 'catch',
      in: 11,
      data: { x: 106, y: 22 },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-incomplete-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-incomplete-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-basket-incomplete-white.png'),
    /* eslint-enable max-len */
  },
};
