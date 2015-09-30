'use strict';

var React = require('react');
var Reflux = require('reflux');
var DraftGroupActivePlayerStore = require("../../stores/draft-group-active-player-store.js");
var renderComponent = require('../../lib/render-component');
// var log = require('../../lib/logging.js');


/**
 * The player detail slideout panel on the draft page. This will display the player info for
 * whatever the DraftGroupActivePlayerStore.activePlayer is.
 */
var DraftPlayerDetail = React.createClass({

  mixins: [
    Reflux.connect(DraftGroupActivePlayerStore)
  ],


  getInitialState: function() {
    return {
      activePlayer: null
    };
  },


  /**
   * Build the player detail panel.
   */
  getPlayerDetail: function() {
    if (this.state.activePlayer) {
      return (
        <div className="cmp-draft-player-detail__player">
          <div className="cmp-draft-player-detail__player-inner">
            <h6 className="cmp-draft-player-detail__team">
              {this.state.activePlayer.team_alias} - {this.state.activePlayer.position}
            </h6>

            <h2 className="cmp-draft-player-detail__name">
              {this.state.activePlayer.name}
            </h2>
          </div>

          <div className="cmp-draft-player-detail__salary">
            <h3>${this.state.activePlayer.salary.toLocaleString('en')}</h3>
          </div>

          <div className="cmp-draft-player-detail__tabs">
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
          </div>
        </div>
      );
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

});


// Render the component.
renderComponent(<DraftPlayerDetail />, '.cmp-draft-player-detail');


module.exports = DraftPlayerDetail;
