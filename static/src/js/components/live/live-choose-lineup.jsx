import LiveLoading from './live-loading';
import Modal from '../modal/modal.jsx';
import moment from 'moment';
import React from 'react';
import forEach from 'lodash/forEach';
import size from 'lodash/size';
import uniq from 'lodash/uniq';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { updateWatchingAndPath } from '../../actions/watching.js';


/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    updateWatchingAndPath,
  }, dispatch),
});

/**
 * Modal window from which a user can select sport + lineup
 * so to observe how the lineup is doing in the live section
 */
export const LiveChooseLineup = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    entries: React.PropTypes.array.isRequired,
    entriesLoaded: React.PropTypes.bool.isRequired,
  },

  getInitialState() {
    return {
      isOpen: true,
      selectedSport: null,
    };
  },

  componentWillMount() {
    // if there's only one entry, then just go to it
    if (size(this.props.entries) === 1) {
      this.selectLineup(this.props.entries[0]);
    }
  },

  componentDidUpdate(prevProps) {
    // if there's only one entry, then just go to it
    const newSize = size(this.props.entries);
    if (newSize !== size(prevProps.entries) && newSize === 1) {
      this.selectLineup(this.props.entries[0]);
    }
  },

  getModalContent() {
    return this.shouldChoseSport() ? this.renderSports() : this.renderLineups();
  },

  shouldChoseSport() {
    if (this.state.selectedSport) {
      return false;
    }

    const differentSports = uniq(
      this.props.entries.map((entry) => entry.sport)
    );

    return differentSports.length > 1;
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

    this.props.actions.updateWatchingAndPath(path, changedFields);
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

    forEach(this.props.entries, (entry) => {
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
    if (!this.props.entriesLoaded) {
      return (<LiveLoading isContestPools={false} />);
    }

    let title = (this.shouldChoseSport()) ? 'Choose a sport' : 'Choose a lineup';
    if (size(this.props.entries) === 0) {
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

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  () => ({}),
  mapDispatchToProps
)(LiveChooseLineup);
