import React from 'react';
import isEmpty from 'lodash/lang/isEmpty';
import { forEach as _forEach } from 'lodash';


const SettingsAddress = React.createClass({

  propTypes: {
    info: React.PropTypes.object.isRequired,
    errors: React.PropTypes.object.isRequired,
    onHandleSubmit: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    return {
      editMode: false,
      info: this.props.info,
    };
  },

  /**
   * if there are no errors comming set edit mode to False
   */
  componentWillReceiveProps(nextProps) {
    if (isEmpty(nextProps.errors)) {
      this.setState({ editMode: false });
    } else {
      this.setState({ editMode: true });
    }

    // Update user info.
    this.setState({ info: nextProps.info });
    // if (!Object.keys(this.state.info).length) {
    //   this.setState({ info: nextProps.info });
    // }
  },

  setEditMode(event) {
    event.preventDefault();
    this.setState({ editMode: true });
  },

  handleSubmit(event) {
    event.preventDefault();
    // get the data from here
    const fullname = this.refs.fullname.value;
    const address1 = this.refs.address1.value;
    const address2 = this.refs.address2.value;
    const city = this.refs.city.value;
    const state = this.refs.state.value;
    const zipcode = this.refs.zipcode.value;

    this.props.onHandleSubmit({
      fullname,
      address1,
      address2,
      city,
      state,
      zipcode,
    });
  },

  renderInfo() {
    return (
      <div className="settings__address form-field">
        <label className="form-field__label">Billing Address</label>
        <div className="form-field__content">
          <p className="form-field__static-content">
            { this.props.info.fullname }<br/>
            { this.props.info.address1 } { this.props.info.address2 }<br/>
            { this.props.info.city }, { this.props.info.state } { this.props.info.zipcode }<br />
            <a href="#" onClick={this.setEditMode}>Edit</a>
          </p>
        </div>
      </div>
    );
  },

  renderErrors(errors) {
    const errorList = [];

    _forEach(errors, (error) => {
      errorList.push(<h6 className="form-field-message__title">{ error }</h6>);
    });

    if (!errorList.length) {
      return '';
    }

    return (
      <div className="form-field-message form-field-message--error form-field-message--settings">
        {errorList}
      </div>
    );
  },

  renderForm() {
    let nameClasses = 'name' in this.props.errors ? 'form-field--error ' : '';
    nameClasses += 'form-field';

    return (
      <form className="form" onSubmit={this.handleSubmit}>
        <div className={nameClasses}>
          <label className="form-field__label" htmlFor="name">Name</label>
          <input
            ref="fullname"
            className="form-field__text-input"
            type="text"
            id="name"
            name="fullname.name"
            defaultValue={this.state.info.fullname}
          />

        {this.renderErrors(this.props.errors.fullname)}
        </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="address1">Address 1</label>
          <input
            ref="address1"
            className="form-field__text-input"
            type="text"
            id="address1"
            name="address1"
            defaultValue={this.state.info.address1}
          />

        {this.renderErrors(this.props.errors.address1)}
        </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="address2">Address 2</label>
          <input
            ref="address2"
            className="form-field__text-input"
            type="text"
            id="address2"
            name="address2"
            defaultValue={this.state.info.address2}
          />
        </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="city">City</label>
          <input
            ref="city"
            className="form-field__text-input"
            type="text"
            id="city"
            name="city"
            defaultValue={this.state.info.city}
          />

        {this.renderErrors(this.props.errors.city)}
        </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="state">State</label>
          <select
            ref="state"
            className="form-field__select"
            id="state"
            name="state"
            defaultValue={this.state.info.state}
          >
            <option value="AL">Alabama</option>
            <option value="AK">Alaska</option>
            <option value="AZ">Arizona</option>
            <option value="AR">Arkansas</option>
            <option value="CA">California</option>
            <option value="CO">Colorado</option>
            <option value="CT">Connecticut</option>
            <option value="DE">Delaware</option>
            <option value="DC">Dist of Columbia</option>
            <option value="FL">Florida</option>
            <option value="GA">Georgia</option>
            <option value="HI">Hawaii</option>
            <option value="ID">Idaho</option>
            <option value="IL">Illinois</option>
            <option value="IN">Indiana</option>
            <option value="IA">Iowa</option>
            <option value="KS">Kansas</option>
            <option value="KY">Kentucky</option>
            <option value="LA">Louisiana</option>
            <option value="ME">Maine</option>
            <option value="MD">Maryland</option>
            <option value="MA">Massachusetts</option>
            <option value="MI">Michigan</option>
            <option value="MN">Minnesota</option>
            <option value="MS">Mississippi</option>
            <option value="MO">Missouri</option>
            <option value="MT">Montana</option>
            <option value="NE">Nebraska</option>
            <option value="NV">Nevada</option>
            <option value="NH">New Hampshire</option>
            <option value="NJ">New Jersey</option>
            <option value="NM">New Mexico</option>
            <option value="NY">New York</option>
            <option value="NC">North Carolina</option>
            <option value="ND">North Dakota</option>
            <option value="OH">Ohio</option>
            <option value="OK">Oklahoma</option>
            <option value="OR">Oregon</option>
            <option value="PA">Pennsylvania</option>
            <option value="RI">Rhode Island</option>
            <option value="SC">South Carolina</option>
            <option value="SD">South Dakota</option>
            <option value="TN">Tennessee</option>
            <option value="TX">Texas</option>
            <option value="UT">Utah</option>
            <option value="VT">Vermont</option>
            <option value="VA">Virginia</option>
            <option value="WA">Washington</option>
            <option value="WV">West Virginia</option>
            <option value="WI">Wisconsin</option>
            <option value="WY">Wyoming</option>
          </select>

          {this.renderErrors(this.props.errors.state)}
        </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="zipcode">Zip Code</label>
          <input
            ref="zipcode"
            className="form-field__text-input"
            type="text"
            id="zipcode"
            name="zipcode"
            defaultValue={this.state.info.zipcode}
          />

        {this.renderErrors(this.props.errors.zipcode)}
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
  },
});


export default SettingsAddress;
