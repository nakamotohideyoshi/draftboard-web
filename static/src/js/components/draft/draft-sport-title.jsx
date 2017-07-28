import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';

const { Provider, connect } = ReactRedux;

function mapStateToProps(state) {
  return {
    theSport: state.draftGroupPlayers.sport,
  };
}

const SportHeader = React.createClass({
  propTypes: {
    theSport: React.PropTypes.string,
  },

  render() {
    if (!this.props.theSport) {
      return null;
    }
    return (
      <div className="sport-title">
        <h2>{this.props.theSport}</h2>
      </div>
    );
  },

});

const SportHeaderConnect = connect(
  mapStateToProps
)(SportHeader);

renderComponent(
  <Provider store={store}>
    <SportHeaderConnect />
  </Provider>,
  '.sidebar--header-title'
);

module.exports = SportHeader;
