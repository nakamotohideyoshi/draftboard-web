'use strict';

import React from 'react';

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
      <section className="pane">
        <div className="pane__close" onClick={this.handleHide}></div>

        <div className="pane__content">

          <div className="pane__header">
            <div className="pane__header__content">
              <div className="pane__title">
                $10,000 - Guaranteed Tiered <br />
                (2,000 to 1st)
              </div>
              <div className="pane__header__info">
                <div>
                  <div>place</div> <br />
                  <span>29th</span>
                </div>
              </div>

              <div className="pane__header__extra-info">
                <div className="m">M</div>
                <div className="g">G</div>
              </div>

              <div className="pane__header__fee-prizes-pool">
                <div><span>Prize</span><div>$150,000</div></div>
                <div><span>Fee</span><div>$25</div></div>
                <div><span>Entrants</span><div>234/1000</div></div>
              </div>
            </div>
          </div>

          <div className="pane__content__tabs">
            <ul>
              <li><a href="#">Payout</a></li>
              <li><a href="#">Scoring</a></li>
              <li><a href="#">Games</a></li>
              <li><a href="#" className="active">Standings</a></li>
            </ul>
          </div>

          <div className="pane__content__tab_content">
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
      </section>
    );
  }
});

export default ResultsPane;
