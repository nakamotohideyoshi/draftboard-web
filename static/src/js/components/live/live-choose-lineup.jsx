import LiveLoading from './live-loading';
import moment from 'moment';
import React from 'react';
import uniq from 'lodash/uniq';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { updateWatchingAndPath } from '../../actions/watching.js';

// assets
require('../../../sass/blocks/live/live-choose-lineup.scss');


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
 * User can select sport + lineup on load
 */
export const LiveChooseLineup = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    lineups: React.PropTypes.array.isRequired,
    lineupsLoaded: React.PropTypes.bool.isRequired,
  },

  getInitialState() {
    return {
      block: 'live-choose-lineup',
      selectedSport: null,
    };
  },

  componentWillMount() {
    // if there's only one lineup, then just go to it
    if (this.props.lineups.length === 1) {
      this.selectLineup(this.props.lineups[0]);
    }
  },

  componentDidUpdate(prevProps) {
    // if there's only one lineup, then just go to it
    const newSize = this.props.lineups.length;
    if (newSize !== prevProps.lineups.length && newSize === 1) {
      this.selectLineup(this.props.lineups[0]);
    }
  },

  getModalContent() {
    return this.shouldChoseSport() ? this.renderSports() : this.renderLineups();
  },

  shouldChoseSport() {
    if (this.state.selectedSport) return false;

    const differentSports = uniq(
      this.props.lineups.map((lineup) => lineup.sport)
    );

    return differentSports.length > 1;
  },

  selectSport(sport) {
    this.setState({ selectedSport: sport });
  },

  selectLineup(lineup) {
    const path = `/live/${lineup.sport}/lineups/${lineup.id}/`;
    const changedFields = {
      draftGroupId: lineup.draftGroup,
      myLineupId: lineup.id,
      sport: lineup.sport,
    };

    this.props.actions.updateWatchingAndPath(path, changedFields);
  },

  sportLineups() {
    const sportLineups = {};

    this.props.lineups.map((lineup) => {
      const sport = lineup.sport;

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
    const { block } = this.state;

    return sportsSorted.map((sport) => (
      <li
        key={sport}
        className={`${block}__option`}
        onClick={this.selectSport.bind(this, sport)}
      >
        <h4 className={`${block}__name`}>{sport.toUpperCase()}</h4>
        <div className={`${block}__info`}>{sportLineups[sport]} lineups</div>
      </li>
    ));
  },

  renderLineups() {
    const { block } = this.state;

    return this.props.lineups.map((lineup) => (
      <li
        key={lineup.id}
        className={`${block}__option`}
        onClick={this.selectLineup.bind(this, lineup)}
      >
        <h4 className={`${block}__name`}>{lineup.name}</h4>
        <div className={`${block}__info`}>
          {moment(lineup.start).format('MMM Do, h:mma')}
        </div>
      </li>
    ));
  },

  render() {
    if (!this.props.lineupsLoaded) {
      return (<LiveLoading isContestPools={false} />);
    }

    const { block } = this.state;

    let title = (this.shouldChoseSport()) ? 'Choose a sport' : 'Choose a lineup';
    if (this.props.lineups.length === 0) title = 'You have no entered lineups.';

    return (
      <section className={block}>
        <div className={`${block}__inner`}>
          <h2 className={`${block}__title`}>{title}</h2>
          <ul className={`${block}__options`}>
            {this.getModalContent()}
          </ul>
        </div>
      </section>
    );
  },
});

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  () => ({}),
  mapDispatchToProps
)(LiveChooseLineup);
