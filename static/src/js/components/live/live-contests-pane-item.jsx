import React from 'react'


/**
 * A single item in the list of contests on LiveContestPane
 */
const LiveContestsPaneItem = React.createClass({

  propTypes: {
    contest: React.PropTypes.object.isRequired,
    onItemClick: React.PropTypes.func.isRequired,
    lineupPotentialEarnings: React.PropTypes.number.isRequired,
  },

  /**
   * Propogating up a click handler to choose this contest to view
   */
  _onClick() {
    this.props.onItemClick(this.props.contest.id)
  },

  render() {
    const contest = this.props.contest
    let moneyLineClass = 'live-winning-graph'

    if (contest.percentageCanWin <= contest.myPercentagePosition) {
      moneyLineClass += ' live-winning-graph--is-losing'
    }

    return (
      <li className="live-contests-pane__contest" key={ contest.id }>
        <div className="live-contests-pane__name">{ contest.name }</div>
        <div className="live-contests-pane__place">
          <span className="live-contests-pane__place--mine">{ contest.myEntryRank }</span> of { contest.entriesCount }
        </div>
        <div className="live-contests-pane__potential-earnings">
          ${ contest.buyin }/${ this.props.lineupPotentialEarnings }
        </div>

        <section className={ moneyLineClass }>
          <div className="live-winning-graph__pmr-line">
            <div className="live-winning-graph__winners" style={{ width: `${contest.percentageCanWin}%` }}></div>
            <div
              className="live-winning-graph__current-position"
              style={{ left: `${contest.myPercentagePosition}%` }}
            ></div>
          </div>
        </section>

        <div className="live-contest-cta" onClick={this._onClick}>Watch Live</div>
      </li>
    )
  },
})

export default LiveContestsPaneItem
