import Modal from '../modal/modal.jsx';
import moment from 'moment';
import React from 'react';
import { forEach as _forEach } from 'lodash';
import { size as _size } from 'lodash';
import { uniqWith as _uniqWith } from 'lodash';


/**
 * Modal window from which a user can select sport + lineup
 * so to observe how the lineup is doing in the live section
 */
const LiveLineupSelectModal = React.createClass({

  propTypes: {
    entriesLoaded: React.PropTypes.bool.isRequired,
    changePathAndMode: React.PropTypes.func.isRequired,
    entries: React.PropTypes.array.isRequired,
  },

  getInitialState() {
    // const sports = this.sportLineups()
    // if all lineups are in same sport, do not show sport selection options
    // const selectedSport = (Object.keys(sports).length === 1) ? Object.keys(sports)[0] : null

    return {
      isOpen: true,
      selectedSport: null,
    };
  },

  componentWillMount() {
    // if there's only one entry, then just go to it
    if (_size(this.props.entries) === 1) {
      this.selectLineup(this.props.entries[0]);
    }
  },

  componentDidUpdate(prevProps) {
    // if there's only one entry, then just go to it
    const newSize = _size(this.props.entries);
    if (newSize !== _size(prevProps.entries) && newSize === 1) {
      this.selectLineup(this.props.entries[0]);
    }
  },

  getModalContent() {
    if (this.state.selectedSport === null) {
      const differentSports = _uniqWith(
        this.props.entries.map((entry) => entry.sport),
        (sport) => sport
      );

      // if there are multiple sports, then make them choose which
      if (differentSports.length > 1) {
        return this.renderSports();
      }
    }

    return this.renderLineups();
  },

  open() {
    this.setState({ isOpen: true });
  },

  close() {
    this.resetSport();
    this.setState({ isOpen: false });
  },

  resetSport() {
    this.setState({ selectedSport: null });
  },

  selectSport(sport) {
    this.setState({ selectedSport: sport });
  },

  selectLineup(entry) {
    const path = `/live/${entry.sport}/lineups/${entry.lineup}/`;
    const changedFields = {
      draftGroupId: entry.draft_group,
      myLineupId: entry.lineup,
      sport: entry.sport,
    };

    this.props.changePathAndMode(path, changedFields);
  },

  /*
   * How many lineups user has for specific sport
   * {
   *   'nba': 10,
   *   'nfl': 5
   * }
   */
  sportLineups() {
    const sportLineups = {};

    _forEach(this.props.entries, (entry) => {
      const sport = entry.sport;

      if (sport in sportLineups) {
        sportLineups[sport] += 1;
      } else {
        sportLineups[sport] = 1;
      }
    });
    return sportLineups;
  },

  renderSports() {
    const sportLineups = this.sportLineups();
    const sportsSorted = Object.keys(sportLineups).sort((x, y) => x > y);

    const sports = sportsSorted.map((sport) => (
      <li
        key={sport}
        className="cmp-live-lineup-select__sport"
        onClick={this.selectSport.bind(this, sport)}
      >
        <h4 className="cmp-live-lineup-select__sport__title">{sport.toUpperCase()}</h4>
        <div className="cmp-live-lineup-select__sport__sub">{sportLineups[sport]} lineups</div>
      </li>
    ));

    return (
      <ul>{sports}</ul>
    );
  },

  renderLineups() {
    const entries = this.props.entries.map((entry) => {
      const name = (entry.lineup_name === undefined) ? 'Example Lineup Name' : entry.lineup_name;

      return (
        <li
          key={entry.id}
          className="cmp-live-lineup-select__lineup"
          onClick={this.selectLineup.bind(this, entry)}
        >
          <h4 className="cmp-live-lineup-select__lineup__title">{name}</h4>
          <div className="cmp-live-lineup-select__lineup__sub">
            {moment(entry.start).format('MMM Do, h:mma')}
          </div>
        </li>
      );
    });

    return (
      <ul>{entries}</ul>
    );
  },

  /*
   * This loading screen shows in lieu of the live section when it takes longer than a second to do an initial load
   * TODO Live - get built out
   *
   * @return {JSXElement}
   */
  renderLoadingScreen() {
    return (
      <div className="live--loading">
        <div className="preload-court" />
        <div className="spinner">
          <div className="double-bounce1" />
          <div className="double-bounce2" />
        </div>
      </div>
    );
  },

  render() {
    if (this.props.entriesLoaded === false) {
      return this.renderLoadingScreen();
    }

    // let title = (this.state.selectedSport) ? 'Choose a lineup' : 'Choose a sport'
    let title = 'Choose a lineup';
    if (_size(this.props.entries) === 0) {
      title = 'You have no entered lineups.';
    }

    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className="cmp-modal-live-lineup-select"
      >

        <div>
          <header className="cmp-modal__header">{title}</header>
          <div className="cmp-live-lineup-select">{this.getModalContent()}</div>
        </div>

      </Modal>
    );
  },
});

export default LiveLineupSelectModal;
