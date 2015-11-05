'use strict';

const React = require('react');
const PureRenderMixin = require('react-addons-pure-render-mixin');


/**
 * Responsible for rendering the contest navigation user info section.
 */
const ContestNavUserInfo = React.createClass({

  mixins: [PureRenderMixin],

  propTypes: {
    name: React.PropTypes.string.isRequired,
    balance: React.PropTypes.string.isRequired
  },

  render() {
    const {name, balance} = this.props;

    return (
      <div className="cmp-contest-nav--user-info">
        <div className="name">{name}</div>
        <div className="balance">
          {balance}
          <div className="add-funds">Add funds</div>
        </div>
      </div>
    );
  }

});


module.exports = ContestNavUserInfo;
