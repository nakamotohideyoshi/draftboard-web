const React = require('react')
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component')


/**
 * The player detail slideout panel on the draft page. This will display the player info for
 * whatever the DraftGroupActivePlayerStore.activePlayer is.
 */
var DraftPlayerDetail = React.createClass({

  propTypes: {
    activePlayer: React.PropTypes.object
  },

  /**
   * Build the player detail panel.
   */
  getPlayerDetail: function() {

    if (this.props.activePlayer) {
      return (
        <div className="cmp-draft-player-detail__player">
          <div className="cmp-draft-player-detail__player-inner">
            <h6 className="cmp-draft-player-detail__team">
              {this.props.activePlayer.team_alias} - {this.props.activePlayer.position}
            </h6>

            <h2 className="cmp-draft-player-detail__name">
              {this.props.activePlayer.name}
            </h2>
          </div>

          <div className="cmp-draft-player-detail__salary">
            <h3>${this.props.activePlayer.salary.toLocaleString('en')}</h3>
          </div>

          <div className="cmp-draft-player-detail__tabs">
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
          </div>
        </div>
      )
    }

    return ('');
  },


  render: function() {
    var playerDetail = this.getPlayerDetail();

    return (
      <div>
        {playerDetail}
      </div>
    );
  }

})



// Redux integration
let {Provider, connect} = ReactRedux

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    activePlayer: state.draftGroupPlayers.focusedPlayer
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
