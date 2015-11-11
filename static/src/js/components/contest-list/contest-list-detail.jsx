import React from 'react'
import {ReactCSSTransitionGroup} from 'react-addons-css-transition-group'


/**
 * Renders a <tr> containing the payout structure details of the selected contest.
 */
var ContestListDetail = React.createClass({

  render: function() {
    return (
      <ReactCSSTransitionGroup
        component="tr"
        transitionName="fade-in"
        transitionAppear="true"
        className="cmp-contest-list__detail cmp-contest-list__row clearfix"
      >
        <td colSpan="9" className="cmp-contest-list__cell" key="details">
          <div className="col col-1">
            <h4 className="cmp-contest-list__detail-header">Payout Structure</h4>
            <ul>
              <li>1st - $100</li>
              <li>2st - $60</li>
              <li>3st - $40</li>
              <li>4st - $30</li>
              <li>5st - $10</li>
              <li>2st - $60</li>
              <li>3st - $40</li>
              <li>4st - $30</li>
              <li>5st - $10</li>
            </ul>
          </div>

          <div className="col col-2">
            <h4 className="cmp-contest-list__detail-header">NBA Scoring</h4>
            <ul>
              <li>1st - $100</li>
              <li>2st - $60</li>
              <li>3st - $40</li>
              <li>4st - $30</li>
              <li>5st - $10</li>
              <li>2st - $60</li>
              <li>3st - $40</li>
              <li>4st - $30</li>
              <li>5st - $10</li>
            </ul>
          </div>
        </td>
      </ReactCSSTransitionGroup>
    )
  }

})


module.exports = ContestListDetail
