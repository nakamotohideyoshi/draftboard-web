export const clip = {
  name: 'qb-shotgun-handoff-fumble-right',
  frame_width: 200,
  frame_height: 120,
  length: 75,
  registration_x: 142,
  registration_y: 68,
  cuepoints: [
    {
      name: 'avatar',
      in: 59,
      data: { x: 65, y: 35, type: 'receiver' },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-fumble-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-fumble-right-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-fumble-right-white.png'),
    /* eslint-enable max-len */
  },
};
