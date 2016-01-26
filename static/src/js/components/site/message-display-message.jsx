import React from 'react'



let MessageDisplayMessage = React.createClass({

  propTypes: {
    message: React.PropTypes.object,
    messageId: React.PropTypes.string,
    removeMessage: React.PropTypes.func
  },


  componentDidMount: function() {
    /**
     * If a ttl was provided, remove the message after the TTL has expired.
     */
    if (!this.props.message.ttl) {
      return
    }

    window.setTimeout(
      () => this.props.removeMessage(this.props.messageId),
      this.props.message.ttl
    )
  },


  // See: https://facebook.github.io/react/tips/dangerously-set-inner-html.html
  createMarkupFromContent: function (content) {
    return {__html: content};
  },


  renderCloseButton: function() {
    if (this.props.message.ttl) {
      return ('')
    }

    return (
      <div
        className="btn-close"
        onClick={this.props.removeMessage.bind(null, this.props.messageId)}
        >
        [X] close
      </div>
    )
  },


  render: function() {
    return (
      <div className={'message ' + this.props.message.level}>
        <div className="message-content">
          <h3
            className="header"
            dangerouslySetInnerHTML={this.createMarkupFromContent(this.props.message.header)}
            ></h3>

          <div
            className="content"
            dangerouslySetInnerHTML={this.createMarkupFromContent(this.props.message.content)}
            ></div>
          {this.renderCloseButton()}
        </div>
      </div>
    )
  }

})

module.exports = MessageDisplayMessage
