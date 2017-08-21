/**
 * Position type filter data.
 *
 * This is used on the draft section to power the position filters on top.
 */
export default {
  nba: [
    { title: 'All', column: 'position', match: '' },
    { title: 'G', column: 'position', match: ['pg', 'sg'] },
    { title: 'F', column: 'position', match: ['sf', 'pf'] },
    { title: 'C', column: 'position', match: 'c' },
  ],
  nfl: [
    { title: 'All', column: 'position', match: '' },
    { title: 'QB', column: 'position', match: 'qb' },
    { title: 'RB', column: 'position', match: ['rb', 'fb'] },
    { title: 'WR', column: 'position', match: 'wr' },
    { title: 'TE', column: 'position', match: 'te' },
    { title: 'FX', column: 'position', match: ['rb', 'wr', 'te', 'fb'] },
  ],
  nhl: [
    { title: 'All', column: 'position', match: '' },
    { title: 'G', column: 'position', match: 'g' },
    { title: 'C', column: 'position', match: 'c' },
    { title: 'F', column: 'position', match: 'f' },
    { title: 'D', column: 'position', match: 'd' },
  ],
  mlb: [
    { title: 'All', column: 'position', match: '' },
    { title: 'SP', column: 'position', match: 'sp' },
    { title: 'C', column: 'position', match: 'c' },
    { title: '1B', column: 'position', match: ['1b', 'dh'] },
    { title: '2B', column: 'position', match: '2b' },
    { title: '3B', column: 'position', match: '3b' },
    { title: 'SS', column: 'position', match: 'ss' },
    { title: 'OF', column: 'position', match: ['lf', 'rf', 'cf'] },
  ],
};
