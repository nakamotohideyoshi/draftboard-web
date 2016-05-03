// import { assert, expect } from 'chai';
// import { assembleCurrentPlayerGameStats } from '../../selectors/live-players';


// describe('livePlayers selectors', () => {
//   it('should return nothing when it does not exist', () => {
//     assert.deepEqual(assembleCurrentPlayerGameStats('foo'), {});
//   });

//   it('should return value of 0 when there is no key in allStats', () => {
//     const allStats = {};
//     const stats = assembleCurrentPlayerGameStats('nba', allStats);
//     expect(stats.assists).to.equal(0);
//   });

//   it('should return all defaults if no stats are passed in', () => {
//     assert.deepEqual(assembleCurrentPlayerGameStats('nba', {}), {
//       assists: 0,
//       blocks: 0,
//       points: 0,
//       rebounds: 0,
//       steals: 0,
//       turnovers: 0,
//     });
//   });

//   it('should return expected fields for nba', () => {
//     const allStats = {
//       assists: 1,
//       blocks: 2,
//       points: 3,
//       rebounds: 4,
//       steals: 5,
//       turnovers: 6,

//       // shouldn't exist in result!
//       foo: 1000,
//       bar: 5000,
//     };

//     assert.deepEqual(assembleCurrentPlayerGameStats('nba', allStats), {
//       assists: 1,
//       blocks: 2,
//       points: 3,
//       rebounds: 4,
//       steals: 5,
//       turnovers: 6,
//     });
//   });
// });
