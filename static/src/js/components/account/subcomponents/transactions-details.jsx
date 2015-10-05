'use strict';

var React = require('react');
var Reflux = require('reflux');

var TransactionsActions = require('../../../actions/transactions-actions');
var TransactionsStore = require('../../../stores/transactions-store');


/**
 * When transaction details is clicked, open side pane.
 * This component is rendered in that side pane
 */
var TransactionsDetails = React.createClass({

  mixins: [
    Reflux.connect(TransactionsStore)
  ],

  propTypes: {
    transaction: React.PropTypes.object.isRequired
  },

  /**
   * Populate transactionDetails in the store on component load.
   * use that transactionDetails from the store afterwards
   */
  getInitialState: function() {
    TransactionsActions.transactionDetails(this.props.transaction.pk);

    return {
      'section': 'standings',
      'transactionDetails': TransactionsStore.data.transactionDetails
    };
  },

  /**
   * Change through tabs (basically change the section type)
   */
  paneTabClicked: function(event) {
    event.preventDefault();
    this.setState({'section': event.target.attributes.href.value});
  },

  /**
   * renderPaneHeader, this is same across different sections (standings/teams/prizes/etc.)
   */
  renderPaneHeader: function() {
    return (
      <div className="pane__header">
        <div className="pane__header__content">
          <div className="pane__transaction_status__completed">completed</div>

          <div className="pane__title">Transaction 009293432</div>
          <div className="pane__header__info">
            <div><span>transaction type</span><div>contest result</div></div>
            <div><span>description</span><div>payout from contest with ID: 2340134j0</div></div>
            <div><span>contest type</span><div>GPP</div></div>
          </div>

          <div className="pane__header__extra-info">
            <div className="pane__header__extra-info__championship">
              <div className="pane__header__extra-info__championship__type">NBA</div>
              <div className="pane__header__extra-info__championship__prize">$150K NBA</div>
              <div className="pane__header__extra-info__championship__championship">Championship</div>
            </div>
          </div>

          <div className="pane__header__fee-prizes-pool">
            <div><span>fee</span><div>$25</div></div>
            <div><span>prize pool</span><div>$150,000</div></div>
            <div><span>date</span><div>03/06/16</div></div>
          </div>
        </div>
      </div>
    );
  },

  /**
   * Tabs options available for every transaction. When clicked on some of the
   * li items here, change state.section to the one clicked and add class `active`
   */
  renderPaneTabsOption: function() {
    var currentSection = this.state.section;

    return (
      <div className="pane__content__tabs">
        <ul>
          <li>
            <a href="standings"
               onClick={this.paneTabClicked}
               className={(currentSection === 'standings')? "active":"" }
            >Standings</a></li>
          <li>
            <a href="teams"
               onClick={this.paneTabClicked}
               className={(currentSection === 'teams')? "active":"" }
            >Teams</a></li>
          <li>
            <a href="prizes"
               onClick={this.paneTabClicked}
               className={(currentSection === 'prizes')? "active":"" }
            >Prizes</a></li>
          <li>
            <a href="scoring"
               onClick={this.paneTabClicked}
               className={(currentSection === 'scoring')? "active":"" }
            >Scoring</a></li>
        </ul>
      </div>
    );
  },

  /**
   * This renders prizes tab content that is to be rendered if this.section === 'prizes'
   */
  renderTransactionPrizes: function() {
    return (
      <div className="pane__content__tab_content">
        <table className="table">
          <thead>
            <tr>
              <th>pos</th>
              <th>user</th>
              <th>pts</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  },

  /**
   * This renders scoring tab content that is to be rendered if this.section === 'scoring'
   */
  renderTransactionScoring: function() {
    return (
      <div className="pane__content__tab_content">
        <table className="table">
          <thead>
            <tr>
              <th>pos</th>
              <th>user</th>
              <th>pts</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  },

  /**
   * This renders standings tab content that is to be rendered if this.section === 'standings'
   */
  renderTransactionStandings: function() {
    return (
      <div className="pane__content__tab_content">
        <table className="table">
          <thead>
            <tr>
              <th>pos</th>
              <th>user</th>
              <th>pts</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
            <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  },

  /**
   * This renders teams tab content that is to be rendered if this.section === 'teams'
   */
  renderTransactionTeams: function() {
    return (
      <div className="pane__content__tab_content">
        <table className="table">
          <thead>
            <tr>
              <th>pos</th>
              <th>user</th>
              <th>pts</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
            <tr>
              <td>1</td>
              <td>Zzzzach</td>
              <td>231</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  },

  /**
   * Render the correct tab content, depending on this.state.section type
   */
  renderPaneTabContent: function() {
    var currentSection = this.state.section;
    if (currentSection === 'standings') {
      return this.renderTransactionStandings();
    } else if (currentSection == 'teams') {
      return this.renderTransactionTeams();
    } else if (currentSection == 'prizes') {
      return this.renderTransactionPrizes();
    } else {
      return this.renderTransactionScoring();
    }
  },

  /**
   * Renders the content that is to be loaded inside the pane
   * NOTE:
   * we add <div class='pane__content'> inside the pane__content DOM.
   * every pane__content is consisted of 3 parts
   * - header
   * - tabs options to be clicked on
   * - tab content
   */
  render: function() {

    var header = this.renderPaneHeader();
    var tabs = this.renderPaneTabsOption();
    var tabContent = this.renderPaneTabContent();

    return (
      <div className="pane__content">
        {header}
        {tabs}
        {tabContent}
      </div>
    );
  }
});


module.exports = TransactionsDetails;
