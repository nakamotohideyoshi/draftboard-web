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


  getGames() {
    const self = this;
    const games = [];

    forEach(this.props.boxScores, (game) => {
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
    } else {
      this.unselectAllTeams();
    }
  },


  /**
   * Scrolls slider left.
   */
  handleScrollLeft() {
    const content = this.refs.content;
    const left = parseInt(content.style.left, 10) | 0;
    this.refs.content.style.left = `${(left + 400)}px`;
  },


  /**
   * Scrolls slider right.
   */
  handleScrollRight() {
    const content = this.refs.content;
    const left = parseInt(content.style.left, 10) | 0;
    content.style.left = `${(left - 400)}px`;
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
        <div className="slider">

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
                  <span className="teamName">All Games</span>
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
