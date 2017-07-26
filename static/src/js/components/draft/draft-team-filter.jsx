import React from 'react';
import moment from 'moment';
import forEach from 'lodash/forEach';
import classNames from 'classnames';


/**
 * A list of games & participating teams, each with a checkboxe that act as filters for the player
 * list.
 */
const DraftTeamFilter = React.createClass({
  propTypes: {
    boxScores: React.PropTypes.object,
    isVisible: React.PropTypes.bool.isRequired,
    onFilterChange: React.PropTypes.func.isRequired,
    selectedTeams: React.PropTypes.array,
    teams: React.PropTypes.object.isRequired,
    sport: React.PropTypes.string,
  },

  getDefaultProps() {
    return {
      selectedTeams: [],
      isVisible: false,
    };
  },
  componentWillMount() {
    this.setState({ selected: '' });
  },

  getGames() {
    const self = this;
    const games = [];

    Object
      .values(this.props.boxScores)
      .sort((p, n) => (new Date(p.start)) - (new Date(n.start)))
      .forEach((game) => {
        const homeClasses = classNames('team home', {
          selected: self.isTeamSelected(self.props.selectedTeams, game.srid_home),
        });
        const awayClasses = classNames('team away', {
          selected: self.isTeamSelected(self.props.selectedTeams, game.srid_away),
        });

        games.push([
          <div
            className="game scroll-item"
            key={game.pk}
            onClick={self.handleGameClick.bind(self, game)}
            ref={`game-${game.pk}`}
          >
            <div className="left">
              <div className={awayClasses} onClick={self.handleTeamClick.bind(self, game.srid_away)}>
                <span className="teamName">{self.getTeamAlias(game.srid_away)}</span>
              </div>

              <div className={homeClasses} onClick={self.handleTeamClick.bind(self, game.srid_home)}>
                <span className="teamName">{self.getTeamAlias(game.srid_home)}</span>
              </div>
            </div>

            <div className="right">
              <div className="start_time">
                {moment(game.start, moment.ISO_8601).format('h:mma')}
              </div>
            </div>
          </div>,
          <div className="separator half"></div>,
        ]);
      });

    return games;
  },


  getAllTeams() {
    const allTeams = [];

    forEach(this.props.boxScores, (game) => {
      allTeams.push(game.srid_home);
      allTeams.push(game.srid_away);
    });

    return allTeams;
  },


  // Safely get the team alias. Oh lord don't hate me.
  getTeamAlias(teamSrid) {
    if (this.props.teams.hasOwnProperty(this.props.sport)) {
      if (this.props.teams[this.props.sport].hasOwnProperty('teams')) {
        if (this.props.teams[this.props.sport].teams.hasOwnProperty(teamSrid)) {
          return this.props.teams[this.props.sport].teams[teamSrid].alias;
        }
      }
    }

    return '';
  },


  scrollDistance: 400,


  handleTeamClick(teamId, e) {
    e.stopPropagation();
    const newTeams = this.props.selectedTeams.slice();

    if (this.isTeamSelected(newTeams, teamId)) {
      this.removeTeamFromList(newTeams, teamId);
    } else {
      newTeams.push(teamId);
    }
    this.handleTeamsChange(newTeams);
  },


  handleAllClick() {
    if (this.getAllTeams().length > this.props.selectedTeams.length) {
      this.selectAllTeams();
      this.setState({ selected: 'selected' });
    } else {
      this.unselectAllTeams();
      this.setState({ selected: '' });
    }
  },


  /**
   * Scrolls slider left.
   */
  handleScrollLeft() {
    const content = this.refs.content;
    const currentOffset = parseInt(content.style.left, 10) | 0;

    // if a full scroll would be less than 0 offset, just go to 0;
    if (Math.abs(currentOffset) < this.scrollDistance) {
      this.refs.content.style.left = 0;
    } else {
      this.refs.content.style.left = `${(currentOffset + this.scrollDistance)}px`;
    }
  },


  /**
   * Scrolls slider right.
   */
  handleScrollRight() {
    const content = this.refs.content;
    const contentWidth = parseInt(this.refs.content.clientWidth, 10) | 0;
    // subtract 40 to account for the arrows that overlay the container.
    const containerWidth = (parseInt(this.refs.container.clientWidth, 10) | 0) - 48;
    const currentOffset = parseInt(content.style.left, 10) | 0;

    if (Math.abs(currentOffset - this.scrollDistance) < (contentWidth - containerWidth)) {
      content.style.left = `${(currentOffset - this.scrollDistance)}px`;
    } else {
      content.style.left = `-${(contentWidth - containerWidth)}px`;
    }
  },


  filterTitle: 'teamFilter',


  selectAllTeams() {
    this.handleTeamsChange(this.getAllTeams());
  },


  unselectAllTeams() {
    this.handleTeamsChange([]);
  },


  isTeamSelected(selectedTeams, teamId) {
    return selectedTeams.indexOf(teamId) !== -1;
  },


  removeTeamFromList(list, team) {
    if (list.indexOf(team) !== -1) {
      list.splice(list.indexOf(team), 1);
    }
  },


  handleGameClick(game) {
    const newTeams = this.props.selectedTeams.slice();

    if (this.isTeamSelected(newTeams, game.srid_home) && this.isTeamSelected(newTeams, game.srid_away)) {
      this.removeTeamFromList(newTeams, game.srid_home);
      this.removeTeamFromList(newTeams, game.srid_away);
    } else {
      this.removeTeamFromList(newTeams, game.srid_home);
      this.removeTeamFromList(newTeams, game.srid_away);
      newTeams.push(game.srid_home);
      newTeams.push(game.srid_away);
    }

    this.handleTeamsChange(newTeams);
  },


  handleTeamsChange(selectedTeams) {
    this.props.onFilterChange(this.filterTitle, 'team_srid', selectedTeams);
  },

  render() {
    if (!this.props.isVisible) {
      return <div></div>;
    }

    return (
      <div className="cmp-draft-team-filter">
        <div className="slider" ref="container">

          <div className="arrow">
            <div className="left-arrow-icon" onClick={this.handleScrollLeft}></div>
          </div>

          <div className="slider-content">
            <div className="slider-content-holder" ref="content">
              <div className="games-list" ref="games-list">
                <div
                  className="game scroll-item allTeams"
                  onClick={this.handleAllClick}
                >
                  <span className={`teamName team ${this.state.selected}`}>All Games</span>
                </div>
                <div className="separator half"></div>
                {this.getGames()}
              </div>
            </div>
          </div>

          <div className="arrow right">
            <div className="right-arrow-icon" onClick={this.handleScrollRight}></div>
          </div>

        </div>
      </div>
    );
  },

});


module.exports = DraftTeamFilter;
