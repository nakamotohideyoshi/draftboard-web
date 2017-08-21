export const clip = {
  name: 'qb-shotgun-handoff-fumble-left',
  frame_width: 190,
  frame_height: 120,
  length: 90,
  registration_x: 142,
  registration_y: 68,
  cuepoints: [
    {
      name: 'avatar',
      in: 59,
      data: { x: 65, y: 35, name: 'receiver' },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-fumble-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-fumble-left-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-fumble-left-white.png'),
    /* eslint-enable max-len */
  },
};
