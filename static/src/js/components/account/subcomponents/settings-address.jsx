'use strict';

var React = require('react');
var Reflux = require('reflux');

var AccountActions = require('../../../actions/account-actions');
var AccountStore = require('../../../stores/account-store');

// TODO: import only things that are used
var _ = require('lodash');


var SettingsAddress = React.createClass({

  mixins: [
    Reflux.connect(AccountStore)
  ],

  componentWillMount: function() {
    AccountActions.userExtraInfo();
  },

  getInitialState: function() {
    return {editMode: false};
  },

  /**
   * Change state.editMode to true (so show form for editing user data)
   */
  setEditMode: function(event) {
    event.preventDefault();
    this.setState({editMode: true});
  },

  handleSubmit: function(event) {
    event.preventDefault();
    // if the following is success repopulate the user info and set editMode to false
    AccountActions.updateExtraInfo(this.postSubmitted);
  },

  /**
   * When form is submitted, callback this function after the ajax is finished
   * if there ARE errors comming from the backend - don't close the form
   */
  postSubmitted: function() {
    if (_.isEmpty(this.state.informationFormErrors)) {
      this.setState({editMode: false});
    } else {
      this.setState({editMode: true});
    }
  },

  /**
   * Show basic info regarding the user address if such exists, or link to add address
   * TODO: if user has no data, render `+Address` link that opens the form
   */
  renderInfo: function() {
    return (
      <div className="form-field">
        <label className="form-field__label">Billing Address</label>
        <div className="form-field__content">
          <p className="form-field__static-content">
            Andrew Smith<br/>
            1317 Oakley St.<br/>
            <a href="#" onClick={this.setEditMode}>Edit</a>
          </p>
        </div>
      </div>
    );
  },

  /**
   * If editMode is true, we should render the form from which the user can edit his credentials
   */
  renderForm: function() {
    if (this.state.information !== undefined) {
      return (
        <form className="form" onSubmit={this.handleSubmit}>
          <div className={'name' in this.state.informationFormErrors ? 'form-field form-field--error' : 'form-field'}>
            <label className="form-field__label" htmlFor="name">Name</label>
            <input className="form-field__text-input" type="text" id="name" name="fullname.name" placeholder="John Doe" />
            { 'name' in this.state.informationFormErrors &&
            <div className="form-field-message form-field-message--error form-field-message--settings">
              <h6 className="form-field-message__title">{ this.state.informationFormErrors.name.title }</h6>
              <p className="form-field-message__description">{ this.state.informationFormErrors.name.description }</p>
            </div>
            }
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="address1">Address 1</label>
            <input className="form-field__text-input" type="text" id="address1" name="address1" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="address2">Address 2</label>
            <input className="form-field__text-input" type="text" id="address2" name="address2" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="city">City</label>
            <input className="form-field__text-input" type="text" id="city" name="city" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="state">State</label>
            <select className="form-field__select" id="state" name="state">
              <option value="hi" selected="selected">hi</option>
              <option value="you" selected="selected">you</option>
              <option value="there" selected="selected">there</option>
            </select>
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="zipcode">Zip Code</label>
            <input className="form-field__text-input" type="text" id="zipcode" name="zipcode" placeholder="32806" />
          </div>

          <input type="submit" className="button--medium" value="Save" />
        </form>
      );
    } else {
      return (
        <div>Loading... (some animation maybe, added as app-action)</div>
      );
    }
  },

  render: function() {
    return (
      <fieldset className="form__fieldset">
        { this.state.editMode &&
          this.renderForm()
        }

        { !this.state.editMode &&
          this.renderInfo()
        }
      </fieldset>
    );
  }
});


module.exports = SettingsAddress;
