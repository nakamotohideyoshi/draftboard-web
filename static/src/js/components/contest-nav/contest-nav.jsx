'use strict';

var React = require('react');
var ReactRedux = require('react-redux');
var Reselect = require('reselect');
var ContestNavFilters = require('./contest-nav-filters.jsx');
var ContestNavContestList = require('./contest-nav-contest-list.jsx');
var renderComponent = require('../../lib/render-component');
var store = require('../../store');


var ContestNav = React.createClass({
  propTypes: {
    contests: React.PropTypes.array.isRequired
  },

  render: function() {
    // Use `this.props.dispatch(action)` for updating the store.
    return (
      <div className="inner">
        <ContestNavFilters />
        <ContestNavContestList contests={this.props.contests} />
      </div>
    );
  }
});


// =============================================================================
// Redux integration

let {Provider, connect} = ReactRedux;
let {createSelector} = Reselect;

// Select portions of the state the component is interested in. Returned
// object will be merged with `this.props` of the connected component.
//
// Here the reselect library is used for creating memoized selectors.
//
let select = createSelector(
  // If all input selectors hit the cache, the pre-computed value for
  // the whole selector is returned and shouldComponentUpdate hook
  // (implemented by `react-redux`) will prevent component from
  // re-rendering.
  (state => state.contests),
  (contests) => {
    return { contests };
  }
);

// Wrap the component to inject dispatch and selected state into it.
var ContestNavConnected = connect(select)(ContestNav);

renderComponent(
  <Provider store={store}>
    <ContestNavConnected />
  </Provider>,
  '.cmp-contest-nav'
);

module.exports = ContestNavConnected;
