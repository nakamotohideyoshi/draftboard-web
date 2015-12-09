import React from 'react'
import Modal from '../modal/modal.jsx'


/**
 * Modal window from which a user can select sport + lineup
 * so to observe how the lineup is doing in the live section
 */
const LiveLineupSelectModal = React.createClass({

  propTypes: {
    lineups: React.PropTypes.array.isRequired
  },

  getInitialState: function() {
    const sports = this.sportLineups()
    // if all lineups are in same sport, do not show sport selection options
    const selectedSport = (Object.keys(sports).length == 1) ? Object.keys(sports)[0] : null

    return {
      isOpen: false,
      selectedSport: selectedSport
    }
  },

  /**
   * array of lineups
   * every lineup should have:
   * - title
   * - sport
   * - pts
   * - pmr
   */
  getDefaultProps: function() {
    return {
      lineups: [
        {
          "id": 1,
          "contest": 2,
          "lineup": 1,
          "title": "Curry's Chicken",
          "draft_group": 1,
          "start": "2015-10-15T23:00:00Z",
          "sport": "nba",
          "pts": 85,
          "pmr": 42
        },
        {
          "id": 2,
          "contest": 2,
          "lineup": 2,
          "title": "Worriers worry",
          "draft_group": 2,
          "start": "2015-10-15T23:00:00Z",
          "sport": "mlb",
          "pts": 85,
          "pmr": 42
        },
        {
          "id": 3,
          "contest": 3,
          "lineup": 3,
          "title": "Kickass your jackass",
          "draft_group": 3,
          "start": "2015-10-15T23:00:00Z",
          "sport": "nba",
          "pts": 102,
          "pmr": 67
        }
      ]
    }
  },

  /*
   * How many lineups user has for specific sport
   * {
   *   'nba': 10,
   *   'nfl': 5
   * }
   */
  sportLineups: function() {
    let sportLineups = {}

    this.props.lineups.map((lineup) => {
      if (lineup.sport in sportLineups) {
        sportLineups[lineup.sport] += 1
      } else {
        sportLineups[lineup.sport] = 1
      }
    })
    return sportLineups
  },

  open: function() {
    this.setState({isOpen: true})
  },

  close: function() {
    this.resetSport();
    this.setState({isOpen: false})
  },

  resetSport: function() {
    this.setState({selectedSport: null})
  },

  selectSport: function(sport) {
    this.setState({selectedSport: sport})
  },

  selectLineup: function(lineup) {
    this.close()
    window.location.assign("/live/lineups/" + lineup.id + "/")
  },

  getModalContent: function() {
    return (this.state.selectedSport === null)? this.renderSports() : this.renderLineups()
  },

  renderSports: function() {
    const sportLineups = this.sportLineups()
    const sportsSorted = Object.keys(sportLineups).sort(function(x, y) { return x > y });

    const sports = sportsSorted.map((sport) => {
      return (
        <li
          key={sport}
          className="cmp-live-lineup-select__sport"
          onClick={this.selectSport.bind(this, sport)}
        >
          <h4 className="cmp-live-lineup-select__sport__title">{sport}</h4>
          <div className="cmp-live-lineup-select__sport__sub">{sportLineups[sport]} lineups</div>
        </li>
      )
    })

    return (
      <ul>{sports}</ul>
    )
  },

  renderLineups: function() {
    const sportLineups = this.props.lineups.filter((lineup) => {
      return lineup.sport === this.state.selectedSport
    })
    const lineups = sportLineups.map((lineup) => {
      const {title, pts, pmr} = lineup
      return (
        <li
          key={lineup.id}
          className="cmp-live-lineup-select__lineup"
          onClick={this.selectLineup.bind(this, lineup)}
        >
          <h4 className="cmp-live-lineup-select__lineup__title">{title}</h4>
          <div className="cmp-live-lineup-select__lineup__sub">{pts} Pts / {pmr} PMR</div>
        </li>
      )
    });

    return (
      <ul>{lineups}</ul>
    )
  },

  render: function() {
    const modalContent = this.getModalContent()
    const title = (this.state.selectedSport) ? "Choose a lineup" : "Choose a sport"

    return (
      <Modal
        isOpen={this.state.isOpen}
        onClose={this.close}
        className="cmp-modal-live-lineup-select"
      >

        <div>
          <header className="cmp-modal__header">{title}</header>
          <div className="cmp-live-lineup-select">{modalContent}</div>
        </div>

      </Modal>
    );
  }

});


export default LiveLineupSelectModal;
