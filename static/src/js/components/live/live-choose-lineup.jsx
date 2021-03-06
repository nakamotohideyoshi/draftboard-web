import LiveLoading from './live-loading';
import moment from 'moment';
import React from 'react';
import uniq from 'lodash/uniq';

// assets
require('../../../sass/blocks/live/live-choose-lineup.scss');


/**
 * User can select sport + lineup on load
 */
export const LiveChooseLineup = React.createClass({

  propTypes: {
    lineups: React.PropTypes.array.isRequired,
    selectLineup: React.PropTypes.func.isRequired,
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
      this.props.selectLineup(this.props.lineups[0]);
    } else {
      this.setSingleSport();
    }
  },

  componentDidUpdate(prevProps) {
    // if there's only one lineup, then just go to it
    const newSize = this.props.lineups.length;
    if (newSize !== prevProps.lineups.length && newSize === 1) {
      this.props.selectLineup(this.props.lineups[0]);
    }
  },

  getModalContent() {
    return this.state.selectedSport ? this.renderLineups() : this.renderSports();
  },

  setSingleSport() {
    const differentSports = uniq(
      this.props.lineups.map((lineup) => lineup.sport)
    );

    if (differentSports.length === 1) this.setState({ selectedSport: differentSports[0] });
  },

  selectSport(sport) {
    this.setState({ selectedSport: sport });
  },

  _onClick(lineup) {
    this.props.selectLineup(lineup);
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
        <svg className={`${block}__arrow`} viewBox="0 0 39.1 21.79">
          <line className={`${block}__arrow-line`} x1="1.5" y1="10.84" x2="37.6" y2="10.84" />
          <line className={`${block}__arrow-line`} x1="27.49" y1="1.5" x2="37.6" y2="10.84" />
          <line className={`${block}__arrow-line`} x1="27.36" y1="20.29" x2="37.6" y2="10.84" />
        </svg>
      </li>
    ));
  },

  renderLineups() {
    const { block, selectedSport } = this.state;

    return this.props.lineups.filter(
      lineup => selectedSport === lineup.sport
    ).map(
      (lineup) => (
        <li
          key={lineup.id}
          className={`${block}__option`}
          onClick={this.props.selectLineup.bind(this, lineup)}
        >
          <h4 className={`${block}__name`}>{lineup.name}</h4>
          <div className={`${block}__info`}>
            {moment(lineup.start).format('MMM Do, h:mma')}
          </div>
          <svg className={`${block}__arrow`} viewBox="0 0 39.1 21.79">
            <line className={`${block}__arrow-line`} x1="1.5" y1="10.84" x2="37.6" y2="10.84" />
            <line className={`${block}__arrow-line`} x1="27.49" y1="1.5" x2="37.6" y2="10.84" />
            <line className={`${block}__arrow-line`} x1="27.36" y1="20.29" x2="37.6" y2="10.84" />
          </svg>
        </li>
      )
    );
  },

  render() {
    if (!this.props.lineupsLoaded) {
      return (<LiveLoading isContestPools={false} />);
    }

    const { block, selectedSport } = this.state;

    let title = selectedSport ? 'Choose a lineup' : 'Choose a sport';
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

export default LiveChooseLineup;
