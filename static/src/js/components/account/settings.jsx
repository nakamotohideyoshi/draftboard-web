"use strict";

var React = require('react');
var renderComponent = require('../../lib/render-component');

var SettingsBase = require('./subcomponents/settings-base.jsx');
var SettingsAddress = require('./subcomponents/settings-address.jsx');


/**
 *
 * The component that is rendered in the base settings section at the account configurations
 * NOTE that this component is combination of 2 others, and the inner components are "smart"
 *
 */
var Settings = React.createClass({

  render: function() {
    return (
      <div>
        <SettingsBase />
        <legend className="form__legend">User Profile</legend>
        <SettingsAddress />
      </div>
    );
  }

});


renderComponent(<Settings />, '#account-settings');


module.exports = Settings;
