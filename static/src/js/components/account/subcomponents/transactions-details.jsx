import React from 'react';


const TransactionsDetails = React.createClass({

  propTypes: {
    transaction: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    return { section: 'standings' };
  },

  componentWillMount() {
    document.body.classList.add('pane-transactions');
  },

  componentWillUnmount() {
    document.body.classList.remove('pane-transactions');
  },

  /**
  * Change through tabs (basically change the section type)
  */
  handleTabChange(event) {
    event.preventDefault();
    this.setState({ section: event.target.attributes.href.value });
  },

  renderPaneHeader() {
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
  renderPaneTabsOption() {
    const currentSection = this.state.section;

    return (
      <div className="pane__content__tabs">
        <ul>
          <li>
            <a href="standings"
              onClick={this.handleTabChange}
              className={(currentSection === 'standings') ? 'active' : '' }
            >Standings</a></li>
          <li>
            <a href="teams"
              onClick={this.handleTabChange}
              className={(currentSection === 'teams') ? 'active' : '' }
            >Teams</a></li>
          <li>
            <a href="prizes"
              onClick={this.handleTabChange}
              className={(currentSection === 'prizes') ? 'active' : '' }
            >Prizes</a></li>
          <li>
            <a href="scoring"
              onClick={this.handleTabChange}
              className={(currentSection === 'scoring') ? 'active' : '' }
            >Scoring</a></li>
        </ul>
      </div>
    );
  },

  renderTransactionPrizes() {
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

  renderTransactionScoring() {
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

  renderTransactionStandings() {
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

  renderTransactionTeams() {
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

  renderPaneTabContent() {
    const currentSection = this.state.section;
    if (currentSection === 'standings') {
      return this.renderTransactionStandings();
    } else if (currentSection === 'teams') {
      return this.renderTransactionTeams();
    } else if (currentSection === 'prizes') {
      return this.renderTransactionPrizes();
    }

    return this.renderTransactionScoring();
  },

  render() {
    const header = this.renderPaneHeader();
    const tabs = this.renderPaneTabsOption();
    const tabContent = this.renderPaneTabContent();

    return (
      <div className="pane__content">
        {header}
        {tabs}
        {tabContent}
      </div>
    );
  },
});


export default TransactionsDetails;
