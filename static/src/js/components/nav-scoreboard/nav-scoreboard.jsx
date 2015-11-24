'use strict';

import React from 'react';
import {Provider, connect} from 'react-redux';

import store from '../../store';
import {fetchUser} from '../../actions/user';
import {fetchEntriesIfNeeded} from '../../actions/entries';
import errorHandler from '../../actions/live-error-handler'
import renderComponent from '../../lib/render-component';

import NavScoreboardLogo from './nav-scoreboard-logo.jsx';
import NavScoreboardMenu from './nav-scoreboard-menu.jsx';
import NavScoreboardSlider from './nav-scoreboard-slider.jsx';
import NavScoreboardFilters from './nav-scoreboard-filters.jsx';
import NavScoreboardUserInfo from './nav-scoreboard-user-info.jsx';
import NavScoreboardSeparator from './nav-scoreboard-separator.jsx';
import NavScoreboardGamesList from './nav-scoreboard-games-list.jsx';
import NavScoreboardLineupsList from './nav-scoreboard-lineups-list.jsx';

import { navScoreboardSelector } from '../../selectors/nav-scoreboard'

import {TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS} from './nav-scoreboard-const.jsx';

import request from 'superagent'
import urlConfig from '../../fixtures/live-config'

const NavScoreboard = React.createClass({

  propTypes: {
    dispatch: React.PropTypes.func.isRequired,
    user: React.PropTypes.object.isRequired,
    games: React.PropTypes.object.isRequired,
    lineups: React.PropTypes.array.isRequired
  },

  getDefaultProps() {
    // Fake contest data.
    return {
      user: {
        name: 'Marshallwild',
        balance: '$542.50'
      },
      games: {
        "MLB": [
          {
            'id': 0,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 1,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 2,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 3,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 4,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 5,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 6,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 7,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 8,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          },
          {
            'id': 9,
            'players': ['ATLL', 'BAL'],
            'time': '7:10PM'
          }
        ],
        "NBA": [
          {
            'id': 8,
            'players': ['ATL', 'BAL'],
            'time': '7:10PM'
          }
        ]
      },
      lineups: [
        {
          'id': 1,
          'name': 'Currys Chicken',
          'contest': 'NBA',
          'time': '7:10PM',
          'pmr': 42,
          'points': 89,
          'balance': '20$'
        },
        {
          'id': 2,
          'name': 'Currys Chicken',
          'contest': 'NBA',
          'time': '7:10PM',
          'pmr': 42,
          'points': 89,
          'balance': '20$'
        }
      ]
    };
  },

  getInitialState() {
    return {
      // Selected option string. SEE: `getSelectOptions`
      selectedOption: null,

      // Selected option type. See type constants above.
      selectedType: null,

      // Selected option key. Subtype from the main type.
      // Competition from games and null for lineups.
      selectedKey: null
    };
  },

  componentWillMount() {
    require('superagent-mock')(request, urlConfig)

    this.props.dispatch(fetchUser());
    this.props.dispatch(
      fetchEntriesIfNeeded()
    ).catch(
      errorHandler
    )
  },

  /**
   * Handle `NavScoreboardFilters` select menu change.
   * @param {String} selectedOption Name of the selected option
   * @param {String} selectedType Type of the selected item
   * @param {String} selectedKey Key of the selected item type
   * @return {Object} options key-value pairs
   */
  handleChangeSelection(selectedOption, selectedType, selectedKey) {
    console.assert(typeof selectedOption === 'string');
    console.assert(typeof selectedType === 'string');
    console.assert(typeof selectedKey === 'string' || selectedKey === null);

    this.setState({selectedOption, selectedType, selectedKey});
  },

  /**
   * Get the options for `NavScoreboardFilters` select menu.
   * @return {Array} options key-value pairs
   */
  getSelectOptions() {
    let options = [];

    Object.keys(this.props.games).forEach((key) => {
      options.push({
        option: key + " GAMES",
        type: TYPE_SELECT_GAMES,
        key: key,
        count: this.props.games[key].length
      });
    });

    options.push({
      option: 'MY LINEUPS',
      type: TYPE_SELECT_LINEUPS,
      key: null,
      count: this.props.lineups.length
    });

    return options;
  },

  /**
   * Render slider contents based on selected filter.
   */
  renderSliderContent() {
    if (this.state.selectedType === TYPE_SELECT_LINEUPS) {
      return <NavScoreboardLineupsList lineups={this.props.lineups} />;
    } else if (this.state.selectedType === TYPE_SELECT_GAMES) {
      let games = this.props.games[this.state.selectedKey];
      return <NavScoreboardGamesList games={games} />;
    } else {
      return null;
    }
  },

  render() {
    const {name, balance} = this.props.user;

    return (
      <div className="inner">
        <NavScoreboardMenu />
        <NavScoreboardSeparator half />
        <NavScoreboardUserInfo name={name} balance={balance} />
        <NavScoreboardSeparator />
        <NavScoreboardFilters
          selected={this.state.selectedOption}
          options={this.getSelectOptions()}
          onChangeSelection={this.handleChangeSelection}
        />
        <NavScoreboardSlider type={this.state.selectedOption}>
          {this.renderSliderContent()}
        </NavScoreboardSlider>
        <NavScoreboardLogo />
      </div>
    );
  }
});


const NavScoreboardConnected = connect(
  navScoreboardSelector
)(NavScoreboard);

renderComponent(
  <Provider store={store}>
    <NavScoreboardConnected />
  </Provider>,
  '.cmp-nav-scoreboard'
)


export default NavScoreboard;
