import React from 'react'
import * as ReactRedux from 'react-redux'
import Modal from '../modal/modal.jsx'
import _ from 'lodash'
import { vsprintf } from 'sprintf-js'
import { updatePath } from 'redux-simple-router'

import { updateLiveMode } from '../../actions/live'



/**
 * Modal window from which a user can select sport + lineup
 * so to observe how the lineup is doing in the live section
 */
const LiveLineupSelectModal = React.createClass({

  propTypes: {
    lineups: React.PropTypes.object.isRequired,
    updateLiveMode: React.PropTypes.func,
    updatePath: React.PropTypes.func
  },

  getInitialState: function() {
    const sports = this.sportLineups()
    // if all lineups are in same sport, do not show sport selection options
    const selectedSport = (Object.keys(sports).length == 1) ? Object.keys(sports)[0] : null

    return {
      isOpen: true,
      selectedSport: selectedSport
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

    _.forEach(this.props.lineups, (lineup) => {
      const sport = lineup.draftGroup.sport

      if (sport in sportLineups) {
        sportLineups[sport] += 1
      } else {
        sportLineups[sport] = 1
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
    this.props.updatePath(vsprintf('/live/lineups/%d/', [lineup.id]))
    this.props.updateLiveMode({
      type: 'lineup',
      draftGroupId: this.props.lineups[lineup.id].draftGroup.id,
      myLineupId: lineup.id
    })
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
    const sportLineups = _.filter(this.props.lineups, (lineup, id) => {
      return lineup.draftGroup.sport === this.state.selectedSport
    })

    console.log('sportLineups', sportLineups, this.state)

    const lineups = sportLineups.map((lineup) => {
      const {points, minutesRemaining} = lineup
      let {name} = lineup

      // TODO have server pass in default names
      if (name === '') {
        name = 'Currys Chicken'
      }

      return (
        <li
          key={lineup.id}
          className="cmp-live-lineup-select__lineup"
          onClick={this.selectLineup.bind(this, lineup)}
        >
          <h4 className="cmp-live-lineup-select__lineup__title">{name}</h4>
          <div className="cmp-live-lineup-select__lineup__sub">{points} Pts / {minutesRemaining} PMR</div>
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


// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {}
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    updateLiveMode: (newMode) => dispatch(updateLiveMode(newMode)),
    updatePath: (path) => dispatch(updatePath(path))
  }
}

// Wrap the component to inject dispatch and selected state into it.
var LiveLineupSelectModalConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveLineupSelectModal)


module.exports = LiveLineupSelectModalConnected
