export const clip = {
  name: 'qb-default-handoff-fumble-left',
  frame_width: 190,
  frame_height: 100,
  length: 63,
  registration_x: 148,
  registration_y: 80,
  cuepoints: [
    {
      name: 'avatar',
      in: 44,
      data: { x: 74, y: 12, type: 'receiver', pause: true },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-fumble-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-fumble-left-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-fumble-left-red.png'),
    /* eslint-enable max-len */
  },
};
