'use strict';

// TODO:
//
// - [ ] remove old contest nav code
//

const React = require('react');

const renderComponent = require('../../lib/render-component');

const ContestNavLogo = require('./contest-nav-logo.jsx');
const ContestNavMenu = require('./contest-nav-menu.jsx');
const ContestNavSlider = require('./contest-nav-slider.jsx');
const ContestNavFilters = require('./contest-nav-filters.jsx');
const ContestNavUserInfo = require('./contest-nav-user-info.jsx');
const ContestNavSeparator = require('./contest-nav-separator.jsx');
const ContestNavGamesList = require('./contest-nav-games-list.jsx');
const ContestNavLineupsList = require('./contest-nav-lineups-list.jsx');


const {TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS} = require('./contest-nav-const.jsx');


const ContestNav = React.createClass({

  propTypes: {
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

  /**
   * Handle `ContestNavFilters` select menu change.
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
   * Get the options for `ContestNavFilters` select menu.
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
      return <ContestNavLineupsList lineups={this.props.lineups} />;
    } else if (this.state.selectedType === TYPE_SELECT_GAMES) {
      let games = this.props.games[this.state.selectedKey];
      return <ContestNavGamesList games={games} />;
    } else {
      return null;
    }
  },

  render() {
    const {name, balance} = this.props.user;

    return (
      <div className="inner">
        <ContestNavMenu />
        <ContestNavSeparator half />
        <ContestNavUserInfo name={name} balance={balance} />
        <ContestNavSeparator />
        <ContestNavFilters
          selected={this.state.selectedOption}
          options={this.getSelectOptions()}
          onChangeSelection={this.handleChangeSelection}
        />
        <ContestNavSlider type={this.state.selectedOption}>
          {this.renderSliderContent()}
        </ContestNavSlider>
        <ContestNavLogo />
      </div>
    );
  }
});


renderComponent(<ContestNav />, '.cmp-contest-nav');

module.exports = ContestNav;
module.exports.TYPE_SELECT_GAMES = TYPE_SELECT_GAMES;
module.exports.TYPE_SELECT_LINEUPS = TYPE_SELECT_LINEUPS;
