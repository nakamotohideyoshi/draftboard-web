import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';

const sportHeader = React.createClass({

  propTypes: {
    sport: React.PropTypes.String,
  },



  render() {
    return (
      <div className="sport-title">
        <h2>{ this.props.sport }</h2>
      </div>
    );
  },

});

const { Provider, connect } = ReactRedux;

const MessageDisplayConnected = connect(
  mapStateToProps,
)(sportHeader);

renderComponent(
  <Provider store={ store }>
    <sportHeader sport="NFL" />
  </Provider>,
  '.sidebar--header-title'
);

module.exports = sportHeader;
