const React = require('react')
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')
import {forEach as _forEach} from 'lodash'
import {focusedPlayerSelector} from '../../selectors/draft-selectors.js'
import {roundUpToDecimalPlace} from '../../lib/utils.js'

/**
 * The player detail slideout panel on the draft page. This will display the player info for
 * whatever the DraftGroupActivePlayerStore.activePlayer is.
 */
var DraftPlayerDetail = React.createClass({

  propTypes: {
    player: React.PropTypes.object
  },


  renderStatsAverage: function() {
    let player = this.props.player;

    if (!Object.keys(player.boxScoreHistory).length) {
      return <div className='player-stats'></div>
    }

    return (
      <div className='player-stats'>
        <ul>
          <li>
            <div className='stat-name'>PPG</div>
            <div className='stat-score'>
              {roundUpToDecimalPlace(player.boxScoreHistory.avg_points, 1)}
            </div>
          </li>
          <li>
            <div className='stat-name'>RPG</div>
            <div className='stat-score'>
              {roundUpToDecimalPlace(player.boxScoreHistory.avg_rebounds, 1)}
            </div>
          </li>
          <li>
            <div className='stat-name'>APG</div>
            <div className='stat-score'>
              {roundUpToDecimalPlace(player.boxScoreHistory.avg_assists, 1)}
            </div>
          </li>
          <li>
            <div className='stat-name'>STLPG</div>
            <div className='stat-score'>
              {roundUpToDecimalPlace(player.boxScoreHistory.avg_steals, 1)}
            </div>
          </li>
          <li>
            <div className='stat-name'>TO</div>
            <div className='stat-score'>
              {roundUpToDecimalPlace(player.boxScoreHistory.avg_turnovers, 1)}
            </div>
          </li>
          <li>
            <div className='stat-name'>FPPG</div>
            <div className='stat-score'>
              {roundUpToDecimalPlace(player.fppg, 1)}
            </div>
          </li>
        </ul>
      </div>
    )
  },


  /**
   * Build the player detail panel.
   */
  getPlayerDetail: function() {

    if (this.props.player) {
      return (
        <div className="player-detail-pane">
          <div className="cmp-draft-player-detail__player-inner">
            <h6 className="cmp-draft-player-detail__team">
              {this.props.player.team_alias} - {this.props.player.position}
            </h6>

            <h2 className="cmp-draft-player-detail__name">
              {this.props.player.name}
            </h2>
          </div>

          <div className="cmp-draft-player-detail__salary">
            <h3>${this.props.player.salary.toLocaleString('en')}</h3>
          </div>

        </div>
      )
    }

    return ('');
  },


  renderPlayerNews: function() {
    let news = []

    if (!Object.keys(this.props.player.news).length) {
      news = (
        <div>No recent news updates.</div>
      )
    }

    _forEach(this.props.player.news, function(item) {
      news.push(
        <article key={item.tsxitem.srid} className="report">
          <header className="header">
            <address className="byline">{item.tsxitem.credit}</address>
            <h5 className="title">{item.tsxitem.title}</h5>
          </header>
          <section className="content">
            <p>{item.tsxitem.content}</p>
          </section>
        </article>
      )
    })

    return (
      <div className="player-reports">
        {news}
      </div>
    )
  },


  render: function() {
    // No player has been selected.
    if (!this.props.player) {
      return (
        <div className="draft-player-detail player-detail-pane">
          <div className="player-pane-inner">Select a Player</div>
        </div>
      )
    }

    let player = this.props.player
    var playerDetail = this.getPlayerDetail();

    return (
      <div className="draft-player-detail player-detail-pane">

        <div className="pane-upper">
          <div className='header-section'>
            <div className="header__player-image" />

            <div className='header__team-role'>
              {player.team_alias} - {player.position}
            </div>
            <div className='header__name'>{ player.name }</div>

            <div className="cmp-draft-player-detail__salary">
              <h3>${this.props.player.salary.toLocaleString('en')}</h3>
            </div>
          </div>

          { this.renderStatsAverage() }
          <div className="next-game">
            <h4 className={'nba-' + this.props.player.team_alias.toLowerCase() + '-1-text' }>{this.props.player.team_alias}</h4>
            <h4 className={'nba-' + this.props.player.team_alias.toLowerCase() + '-2-text' }>{this.props.player.team_alias}</h4>
          </div>
        </div>

        <div className="pane-lower">
          <ul className="tab-nav">
            <li>Reports</li>
            <li>Splits</li>
          </ul>

          <div className="tab-content">
            {this.renderPlayerNews()}
          </div>
        </div>

      </div>
    );
  }

})



// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    player: focusedPlayerSelector(state)
  }
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {}
}

// Wrap the component to inject dispatch and selected state into it.
var DraftPlayerDetailConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftPlayerDetail)

// Render the component.
renderComponent(
  <Provider store={store}>
    <DraftPlayerDetailConnected />
  </Provider>,
  '.cmp-draft-player-detail'
)


module.exports = DraftPlayerDetail
