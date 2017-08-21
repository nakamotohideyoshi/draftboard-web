import merge from 'lodash/merge';
import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveHistoryListPBP from '../../../components/live/live-history-list-pbp.jsx';

/**
 * Tests for LiveAnimationArea
 */
describe('<LiveHistoryListPBP /> Component', () => {
  const defaultProps = {
    id: 123,
    sport: 'nba',
    description: 'Jimmy Butler makes two point reverse layup',
    lineup: 'mine',
    players: [
      {
        fp: 1,
        srid: '0e163d44-67a7-4107-9421-5333600166bb',
        lineup: 'mine',
      },
    ],
    game: {
      awayTeamAlias: 'OKC',
      homeTeamAlias: 'MIL',
      description: 'Jimmy Butler makes two point reverse layup',
      period: 1,
      clock: '9:59',
    },
  };

  it('should render the correct game time during the first quarter', () => {
    const wrapper = mount(<LiveHistoryListPBP {...defaultProps} />);
    expect(wrapper.find('.live-history-list-pbp__when').text()).to.equal('Q1 9:59');
  });

  it('should render the correct game time during overtime', () => {
    const props = merge({}, defaultProps);
    props.game.period = 5;
    const wrapper = mount(<LiveHistoryListPBP {...props} />);
    expect(wrapper.find('.live-history-list-pbp__when').text()).to.equal('OT 9:59');
  });

  it('should render the correct game time during double overtime', () => {
    const props = merge({}, defaultProps);
    props.game.period = 6;
    const wrapper = mount(<LiveHistoryListPBP {...props} />);
    expect(wrapper.find('.live-history-list-pbp__when').text()).to.equal('2OT 9:59');
  });
});
