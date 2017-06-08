// Roster templates used for empty lineup cards and lineup validation.
export const rosterTemplates = {
  nfl: [
    { idx: 0, name: 'QB', positions: ['QB'] },
    { idx: 1, name: 'RB', positions: ['RB', 'FB'] },
    { idx: 2, name: 'RB', positions: ['RB', 'FB'] },
    { idx: 3, name: 'WR', positions: ['WR'] },
    { idx: 4, name: 'WR', positions: ['WR'] },
    { idx: 5, name: 'TE', positions: ['TE'] },
    { idx: 6, name: 'FX', positions: ['RB', 'FB', 'WR', 'TE'] },
    { idx: 7, name: 'FX', positions: ['RB', 'FB', 'WR', 'TE'] },
  ],
  nba: [
    { idx: 0, name: 'G', positions: ['PG', 'SG'] },
    { idx: 1, name: 'G', positions: ['PG', 'SG'] },
    { idx: 2, name: 'F', positions: ['SF', 'PF'] },
    { idx: 3, name: 'F', positions: ['SF', 'PF'] },
    { idx: 4, name: 'C', positions: ['C'] },
    { idx: 5, name: 'FX', positions: ['PG', 'SG', 'SF', 'PF', 'C'] },
    { idx: 6, name: 'FX', positions: ['PG', 'SG', 'SF', 'PF', 'C'] },
    { idx: 7, name: 'FX', positions: ['PG', 'SG', 'SF', 'PF', 'C'] },
  ],
  nhl: [
    { idx: 0, name: 'F', positions: ['C', 'LW', 'RW'] },
    { idx: 1, name: 'F', positions: ['C', 'LW', 'RW'] },
    { idx: 2, name: 'F', positions: ['C', 'LW', 'RW'] },
    { idx: 3, name: 'D', positions: ['D'] },
    { idx: 4, name: 'D', positions: ['D'] },
    { idx: 5, name: 'FX', positions: ['C', 'D', 'LW', 'RW'] },
    { idx: 6, name: 'FX', positions: ['C', 'D', 'LW', 'RW'] },
    { idx: 7, name: 'G', positions: ['G'] },
  ],
  mlb: [
    { idx: 0, name: 'SP', positions: ['SP'] },
    { idx: 1, name: 'C', positions: ['C'] },
    { idx: 2, name: '1B', positions: ['1B', 'DH'] },
    { idx: 3, name: '2B', positions: ['2B'] },
    { idx: 4, name: '3B', positions: ['3B'] },
    { idx: 5, name: 'SS', positions: ['SS'] },
    { idx: 6, name: 'OF', positions: ['LF', 'CF', 'RF'] },
    { idx: 7, name: 'OF', positions: ['LF', 'CF', 'RF'] },
    { idx: 8, name: 'OF', positions: ['LF', 'CF', 'RF'] },
  ],
};


// Salary cap for each sport.
export const salaryCaps = {
  nba: 50000,
  nfl: 50000,
  nhl: 50000,
  mlb: 50000,
};


/**
 * When saving a lineup, run through various validations.
 * @param  {Array} lineup A list of players.
 * @return {Array}        A list of errors.
 */
export function validateLineup(lineup) {
  const errors = [];
  // Does each slot have a player in it?
  for (const slot of lineup) {
    if (!slot.player) {
      errors.push('lineup is not completely filled.');
      // Immediately exit because a missing player can break subsequent validation.
      return errors;
    }
  }

  // Return any errors we've found.
  return errors;
}
