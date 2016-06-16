import React from 'react';
import store from '../../store';
import * as ReactRedux from 'react-redux';
import renderComponent from '../../lib/render-component';
import { addMessage, removeMessage, clearMessages } from '../../actions/message-actions.js';
import forEach from 'lodash/forEach';
import MessageDisplayMessage from './message-display-message.jsx';
const { Provider, connect } = ReactRedux;
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    messages: state.messages,
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    addMessage: (content, level) => dispatch(addMessage(content, level)),
    removeMessage: (messageId) => dispatch(removeMessage(messageId)),
    clearMessages: () => dispatch(clearMessages()),
  };
}


/**
 * A global message display. This shows messages in state.messages to the user. Message display
 * styles are based on the message.level. Available styles are in cmp-message-display.scss.
 */
const MessageDisplay = React.createClass({

  propTypes: {
    messages: React.PropTypes.object,
    addMessage: React.PropTypes.func,
    removeMessage: React.PropTypes.func,
    clearMessages: React.PropTypes.func,
  },


  renderMessages() {
    const self = this;
    const messages = [];

    forEach(this.props.messages, (message, messageId) => {
      messages.push(
        <MessageDisplayMessage
          message={message}
          messageId={messageId}
          removeMessage={self.props.removeMessage}
          key={messageId}
        />
      );
    });

    return messages;
  },


  render() {
    return (
      <div className="message-list">
        <ReactCSSTransitionGroup
          transitionName="message-transition"
          transitionEnterTimeout={500}
          transitionLeaveTimeout={300}
        >
          {this.renderMessages()}
        </ReactCSSTransitionGroup>
      </div>
    );
  },

});


const MessageDisplayConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(MessageDisplay);

renderComponent(
  <Provider store={store}>
    <MessageDisplayConnected />
  </Provider>,
  '.cmp-message-display'
);


module.exports = MessageDisplay;
