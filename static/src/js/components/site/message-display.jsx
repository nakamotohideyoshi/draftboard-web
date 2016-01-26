import React from 'react'
import store from '../../store'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import {addMessage, removeMessage, clearMessages} from '../../actions/message-actions.js'
import {forEach as _forEach} from 'lodash'
const {Provider, connect} = ReactRedux



/**
 * A global message display. This shows messages in state.messages to the user. Message display
 * styles are based on the message.level. Available styles are in cmp-message-display.scss.
 */
let MessageDisplay = React.createClass({

  propTypes: {
    messages: React.PropTypes.object,
    addMessage: React.PropTypes.func,
    removeMessage: React.PropTypes.func,
    clearMessages: React.PropTypes.func
  },

  // See: https://facebook.github.io/react/tips/dangerously-set-inner-html.html
  createMarkupFromContent: function (content) {
    return {__html: content};
  },


  renderMessages: function() {
    let messages = []

    _forEach(this.props.messages, function(message, messageId) {
      messages.push(
        <div className={'message ' + message.level} key={messageId}>
          <div className="message-content">
            <div dangerouslySetInnerHTML={this.createMarkupFromContent(message.content)}></div>
            <div
              className="btn-close"
              onClick={this.props.removeMessage.bind(null, messageId)}
            >
              [X] close
            </div>
          </div>
        </div>
      )
    }.bind(this))

    return messages
  },


  render: function() {
    return (
      <div className="message-list">
        {this.renderMessages()}
      </div>
    )
  }

})


function mapStateToProps(state) {
  return {
    messages: state.messages
  }
}

function mapDispatchToProps(dispatch) {
  return {
    addMessage: (content, level) => dispatch(addMessage(content, level)),
    removeMessage: (messageId) => dispatch(removeMessage(messageId)),
    clearMessages: () => dispatch(clearMessages())
  }
}

var MessageDisplayConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(MessageDisplay)

renderComponent(
  <Provider store={store}>
    <MessageDisplayConnected />
  </Provider>,
  '.cmp-message-display'
)



module.export = MessageDisplay
