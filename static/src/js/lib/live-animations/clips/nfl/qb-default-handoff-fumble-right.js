export const clip = {
  name: 'qb-default-handoff-fumble-right',
  frame_width: 190,
  frame_height: 100,
  length: 63,
  registration_x: 148,
  registration_y: 80,
  cuepoints: [
    {
      name: 'avatar',
      in: 44,
      data: { x: 70, y: 14, in: 44, name: 'receiver' },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-fumble-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-fumble-right-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-fumble-right-white.png'),
    /* eslint-enable max-len */
  },
};
