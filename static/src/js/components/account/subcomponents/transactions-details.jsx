import React from 'react';
import { Provider, connect } from 'react-redux';
import renderComponent from '../../../lib/render-component.js';
import store from '../../../store.js';
import { focusedTransactionSelector } from '../../../selectors/focused-transaction-selector.js';


function mapStateToProps(state) {
  return {
    transaction: focusedTransactionSelector(state),
  };
}

function mapDispatchToProps() {
  return {

  };
}


const TransactionsDetails = React.createClass({

  propTypes: {
    transaction: React.PropTypes.object,
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

          <div className="pane__title">Transaction #{this.props.transaction.id}</div>

          <div className="pane__header__info">
            <div><span>transaction type</span> <div>contest result</div></div>
            <div><span>description</span> <div>transaction - description</div></div>
            <div><span>contest type</span> <div>{this.props.transaction.details[0].type}</div></div>
          </div>

          <div className="pane__header__extra-info">
            <div className="pane__header__extra-info__championship">
              <div className="pane__header__extra-info__championship__type">FPO NBA</div>
              <div className="pane__header__extra-info__championship__prize">
              <div>FPO contest title</div>
              <div className="pane__header__extra-info__championship__championship">FPO Championship</div>
            </div>
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
    if (!this.props.transaction) {
      return (
        <div><h3>Please select a Transaction.</h3></div>
      );
    }

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


const TransactionsDetailsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(TransactionsDetails);

renderComponent(
  <Provider store={store}>
    <TransactionsDetailsConnected />
  </Provider>,
  '.cmp-transactions-details'
);


module.exports = TransactionsDetails;
