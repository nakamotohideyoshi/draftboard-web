'use strict';

import React from 'react';
const isEmpty = require('lodash/lang/isEmpty')


const SettingsAddress = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    errors: React.PropTypes.object.isRequired,
    onHandleSubmit: React.PropTypes.func.isRequired
  },

  getInitialState() {
    return {editMode: false}
  },

  /**
   * if there are no errors comming set edit mode to False
   */
  componentWillReceiveProps(nextProps) {
    if (isEmpty(nextProps.errors)) {
      this.setState({editMode: false})
    } else {
      this.setState({editMode: true})
    }
  },

  setEditMode(event) {
    event.preventDefault();
    this.setState({editMode: true});
  },

  handleSubmit(event) {
    event.preventDefault();
    // TODO: get form data, and send it as arg
    this.props.onHandleSubmit({})
  },

  renderInfo() {
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

  renderForm() {
    return (
      <form className="form" onSubmit={this.handleSubmit}>
        <div className={'name' in this.props.errors ? 'form-field form-field--error' : 'form-field'}>
          <label className="form-field__label" htmlFor="name">Name</label>
          <input className="form-field__text-input" type="text" id="name" name="fullname.name" placeholder="John Doe" />
          { 'name' in this.props.errors &&
          <div className="form-field-message form-field-message--error form-field-message--settings">
            <h6 className="form-field-message__title">{ this.props.errors.name.title }</h6>
            <p className="form-field-message__description">{ this.props.errors.name.description }</p>
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
  },

  render() {
    return (
      <fieldset className="form__fieldset">
        { this.state.editMode && this.renderForm() }
        { !this.state.editMode && this.renderInfo() }
      </fieldset>
    );
  }
});


export default SettingsAddress;
