import _ from 'lodash'
import Modal from '../modal/modal.jsx'
import React from 'react'
import moment from 'moment'


/**
 * Modal window from which a user can select sport + lineup
 * so to observe how the lineup is doing in the live section
 */
const LiveLineupSelectModal = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    entries: React.PropTypes.array.isRequired,
  },

  getInitialState() {
    // const sports = this.sportLineups()
    // if all lineups are in same sport, do not show sport selection options
    // const selectedSport = (Object.keys(sports).length === 1) ? Object.keys(sports)[0] : null

    return {
      isOpen: true,
      selectedSport: 'nba',
    }
  },

  getModalContent() {
    return (this.state.selectedSport === null) ? this.renderSports() : this.renderLineups()
  },

  open() {
    this.setState({ isOpen: true })
  },

  close() {
    this.resetSport();
    this.setState({ isOpen: false })
  },

  resetSport() {
    this.setState({ selectedSport: null })
  },

  selectSport(sport) {
    this.setState({ selectedSport: sport })
  },

  selectLineup(entry) {
    const path = `/live/lineups/${entry.lineup}/`
    const changedFields = {
      draftGroupId: entry.draft_group,
      myLineupId: entry.lineup,
    }

    this.props.changePathAndMode(path, changedFields)
  },

  /*
   * How many lineups user has for specific sport
   * {
   *   'nba': 10,
   *   'nfl': 5
   * }
   */
  sportLineups() {
    const sportLineups = {}

    _.forEach(this.props.entries, (lineup) => {
      const sport = lineup.draftGroup.sport

      if (sport in sportLineups) {
        sportLineups[sport] += 1
      } else {
        sportLineups[sport] = 1
      }
    })
    return sportLineups
  },

  renderSports() {
    const sportLineups = this.sportLineups()
    const sportsSorted = Object.keys(sportLineups).sort((x, y) => x > y);

    const sports = sportsSorted.map((sport) => (
      <li
        key={sport}
        className="cmp-live-lineup-select__sport"
        onClick={this.selectSport.bind(this, sport)}
      >
        <h4 className="cmp-live-lineup-select__sport__title">{sport}</h4>
        <div className="cmp-live-lineup-select__sport__sub">{sportLineups[sport]} lineups</div>
      </li>
    ))

    return (
      <ul>{sports}</ul>
    )
  },

  renderLineups() {
    // const sportLineups = _.filter(
    //  this.props.lineups, (lineup) => lineup.draftGroup.sport === this.state.selectedSport
    // )
    const lineups = this.props.entries.map((lineup) => {
      const name = (lineup.name === undefined) ? 'Example Lineup Name' : lineup.name

      return (
        <li
          key={lineup.id}
          className="cmp-live-lineup-select__lineup"
          onClick={this.selectLineup.bind(this, lineup)}
        >
          <h4 className="cmp-live-lineup-select__lineup__title">{name}</h4>
          <div className="cmp-live-lineup-select__lineup__sub">
            {moment(lineup.start).format('MMM Do, h:mma')} EST
          </div>
        </li>
      )
    });

    return (
      <ul>{lineups}</ul>
    )
  },

  render() {
    // let title = (this.state.selectedSport) ? 'Choose a lineup' : 'Choose a sport'
    let title = 'Choose a lineup'
    if (_.size(this.props.entries) === 0) {
      title = 'You have no entered lineups.'
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
})

export default LiveLineupSelectModal
