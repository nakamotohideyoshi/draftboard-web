import React from 'react';


const SettingsEmailNotifications = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    editMode: React.PropTypes.bool.isRequired,
  },

  renderInfo() {
    return (
      <fieldset className="form__fieldset">
      <div className="form-field form-field--with-help">
        <label className="form-field__label" htmlFor="notifications">Email Notifications</label>

        <div className="form-field__content">
          <p className="form-field__info">
            Master cleanse Thundercats forage small batch Williamsburg. YOLO migas farm-to-table Vice, heirloom trust
            fund lo-fi.
          </p>

          <ul>
            <li>Contests are starting</li>
            <li>Contest victories</li>
            <li>Newsletter</li>
            <li>Upcoming contetsts</li>
          </ul>
        </div>
      </div>
      </fieldset>
    );
  },

  renderForm() {
    return (
      <div className="form-field form-field--with-help">
        <label className="form-field__label" htmlFor="notifications">Email Notifications</label>

        <div className="form-field__content">
          <p className="form-field__info">
            Master cleanse Thundercats forage small batch Williamsburg. YOLO migas farm-to-table Vice, heirloom trust
            fund lo-fi.
          </p>

          <ul className="radio-button-list">
            <li>
              <div className="radio-button-list__header-label">Off</div>
              <div className="radio-button-list__header-label">On</div>
            </li>

            <li>
              <div className="radio-button-list__title">
                Contests are starting
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio"
                  id="contests--starting2"
                  name="email_notification_contests_starting"
                  value="off"
                  defaultChecked="checked"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting2">Off</label>
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio" id="contests--starting1"
                  name="email_notification_contests_starting"
                  value="on"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting1">On</label>
              </div>
            </li>

            <li>
              <div className="radio-button-list__title">
                Contests victories
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio" id="contests--starting4"
                  name="email_notification_contest_victories"
                  value="off"
                  defaultChecked="checked"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting4">Off</label>
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio"
                  id="contests--starting3"
                  name="email_notification_contest_victories"
                  value="on"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting3">On</label>
              </div>
            </li>

            <li>
              <div className="radio-button-list__title">
                Newsletter
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio"
                  id="contests--starting6"
                  name="email_notification_newsletter"
                  value="off"
                  defaultChecked="checked"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting6">Off</label>
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio"
                  id="contests--starting5"
                  name="email_notification_newsletter"
                  value="on"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting5">On</label>
              </div>
            </li>

            <li>
              <div className="radio-button-list__title">
                Upcoming Contests
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio"
                  id="contests--starting8"
                  name="email_notification_upcoming_contests"
                  value="off"
                  defaultChecked="checked"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting8">Off</label>
              </div>

              <div className="radio-button-list__button-container pull-right">
                <input
                  className="radio-button-list__input"
                  type="radio"
                  id="contests--starting7"
                  name="email_notification_upcoming_contests"
                  value="on"
                />
                <label className="radio-button-list__label" htmlFor="contests--starting7">On</label>
              </div>
            </li>
          </ul>
        </div>
      </div>
    );
  },

  render() {
    return (
      <div>
        { this.props.editMode && this.renderForm() }
        { !this.props.editMode && this.renderInfo() }
      </div>
    );
  },

});


export default SettingsEmailNotifications;
