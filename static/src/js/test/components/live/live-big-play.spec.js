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
    event: {
      description: 'Jimmy Butler makes two point reverse layup',
      eventPlayers: [
        '0e163d44-67a7-4107-9421-5333600166bb',
      ],
      pbp: {
        description: 'Jimmy Butler makes two point reverse layup',
        clock: '9:59',
      },
      whichSide: 'mine',
      homeScoreStr: 'MIL 50',
      awayScoreStr: 'OKC 56',
      winning: 'away',
      playerFPChanges: {},
      when: '9:59',
      quarter: 1,
      game: {
        away: 'OKC',
        home: 'MIL',
      },
      stats: [],
    },
  };

  it('should render the correct game time during the first quarter', () => {
    const wrapper = mount(<LiveHistoryListPBP {...defaultProps} />);
    expect(wrapper.find('.live-history-list-pbp__when').text()).to.equal('Q1 9:59');
  });

  it('should render the correct game time during overtime', () => {
    const props = merge({}, defaultProps);
    props.event.quarter = 5;
    const wrapper = mount(<LiveHistoryListPBP {...props} />);
    expect(wrapper.find('.live-history-list-pbp__when').text()).to.equal('OT 9:59');
  });

  it('should render the correct game time during double overtime', () => {
    const props = merge({}, defaultProps);
    props.event.quarter = 6;
    const wrapper = mount(<LiveHistoryListPBP {...props} />);
    expect(wrapper.find('.live-history-list-pbp__when').text()).to.equal('2OT 9:59');
  });
});
