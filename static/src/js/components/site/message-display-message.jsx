import React from 'react';


/**
 * A single message for the MessageDisplayMessage component.
 */
const MessageDisplayMessage = React.createClass({

  propTypes: {
    message: React.PropTypes.object,
    messageId: React.PropTypes.string,
    removeMessage: React.PropTypes.func,
  },


  componentDidMount() {
    /**
     * If a ttl was provided, remove the message after the TTL has expired.
     */
    if (!this.props.message.ttl) {
      return;
    }

    window.setTimeout(
      () => this.props.removeMessage(this.props.messageId),
      this.props.message.ttl
    );
  },


  // See: https://facebook.github.io/react/tips/dangerously-set-inner-html.html
  createMarkupFromContent(content) {
    return { __html: content };
  },


  renderCloseButton() {
    if (this.props.message.ttl) {
      return ('');
    }

    return (
      <div
        className="btn-close"
        onClick={this.props.removeMessage.bind(null, this.props.messageId)}
      ></div>
    );
  },


  renderContent(content) {
    if (content) {
      return (
        <div
          className="content"
          dangerouslySetInnerHTML={this.createMarkupFromContent(content)}
        />
      );
    }

    return '';
  },


  render() {
    return (
      <div className={`message ${this.props.message.level}`}>
        <div className={`message-content msg-${this.props.messageId}`}>
          <h3 className="header">
            <span
              className="text"
              dangerouslySetInnerHTML={this.createMarkupFromContent(this.props.message.header)}
            ></span>
          </h3>

          {this.renderContent(this.props.message.content)}
          {this.renderCloseButton()}
        </div>
      </div>
    );
  },


});

module.exports = MessageDisplayMessage;
