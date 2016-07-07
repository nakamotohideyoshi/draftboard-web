import assert from 'assert';
import log from '../../lib/logging';
import { reduxLoggerLevel } from '../../lib/logging';


describe('lib.logging', () => {
  it('should always have custom getLoggers set to SILENT in master branch', () => {
    // 4 is ERROR, 1 is DEBUG
    assert.equal(log.getLogger('action').getLevel(), 5);
    assert.equal(log.getLogger('app').getLevel(), 1);
    assert.equal(log.getLogger('app-state-store').getLevel(), 5);
    assert.equal(log.getLogger('component').getLevel(), 5);
    assert.equal(log.getLogger('selector').getLevel(), 5);
  });

  it('should never have redux-logging on production', () => {
    // 4 is ERROR, and can never be greater than
    assert.equal(reduxLoggerLevel < 4, true);
  });
});
