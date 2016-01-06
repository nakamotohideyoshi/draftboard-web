'use strict';

import React from 'react';
import PrizeStructure from '../contest-list/prize-structure.jsx'


const ResultsPane = React.createClass({

  propTypes: {
    onHide: React.PropTypes.func.isRequired
  },

  componentWillMount() {
    document.body.classList.add('results-pane');
  },

  componentWillUnmount() {
    document.body.classList.remove('results-pane');
  },

  handleHide() {
    this.props.onHide();
  },

  render() {
    return (
      <section className="pane pane--contest-detail pane--contest-results">
        <div className="pane__close" onClick={this.handleHide}></div>

        <div className="pane__content">
          <div className="pane-upper">
            <div className="header">
              <div className="header__content">
                <div className="title">
                  $10,000 - Guaranteed Tiered <br />
                (2,000 to 1st)
              </div>
              <div className="header__info">
                <div  className="header__place">
                  <div className="info-title">place</div>
                  <span>29th</span>
                </div>
              </div>

              <div className="header__extra-info">
                <div className="m badge">M</div>
                <div className="g badge">G</div>
              </div>

              <div className="header__fee-prizes-pool">
                <div><span className="info-title">Prize</span><div>$150,000</div></div>
                <div><span className="info-title">Fee</span><div>$25</div></div>
                <div><span className="info-title">Entrants</span><div>234/1000</div></div>
              </div>
            </div>
          </div>
          </div>

          <div className="pane-lower">
            <div className="tab-nav">
              <ul>
                <li>Payout</li>
                <li>Scoring</li>
                <li>Games</li>
                <li className="active">Standings</li>
              </ul>
            </div>

            <div className="tab-content">
              <table className="table">
                <thead>
                  <tr>
                    <th>entry</th>
                    <th>prize</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Buster66</td>
                    <td>$12,000</td>
                  </tr>
                  <tr>
                    <td>Buster66</td>
                    <td>$12,000</td>
                  </tr>
                  <tr>
                    <td>Buster66</td>
                    <td>$12,000</td>
                  </tr>
                  <tr>
                    <td>Buster66</td>
                    <td>$12,000</td>
                  </tr>
                  <tr>
                    <td>Buster66</td>
                    <td>$12,000</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </section>
    );
  }
});

export default ResultsPane;
