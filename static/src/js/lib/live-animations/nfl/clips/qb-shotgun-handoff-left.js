export const clip = {
  name: 'qb-shotgun-handoff-left',
  frame_width: 190,
  frame_height: 120,
  length: 90,
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
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-left-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-left-red.png'),
  },
};
