import React from 'react';
import * as ReactRedux from 'react-redux';
import { bindActionCreators } from 'redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { addMessage } from '../../actions/message-actions.js';
import { receiveUserLimits } from '../../actions/user.js';
import { fetchUserLimits } from '../../actions/user.js';
const { Provider, connect } = ReactRedux;
import request from 'superagent';
import Cookies from 'js-cookie';
const pageText = [
  {
    boldText: 'Deposit Limit: ',
    text: 'Please select a deposit limit that you would like applied to your account.',
  },
  {
    boldText: 'Contest Entry Alert: ',
    text: 'Please select the number of entries and period for which you\'d like to be alerted.',
  },
  {
    boldText: 'Contest Entry Limit: ',
    text: 'Please select a limit for the number of contests you may enter in a time period.',
  },
  {
    boldText: 'Contest Entry Limit: ',
    text: 'Please select the appropriate contest entry fee.',
  },
];

function mapStateToProps(state) {
  return {
    csrftoken: Cookies.get('csrftoken'),
    userLimits: state.user.user.userLimits,
    currentLimits: state.user.user.currentLimits,
    selectedLimits: state.user.user.selectedLimits,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators({
      addMessage,
      receiveUserLimits,
    }, dispatch),
  };
}


const Limits = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    userLimits: React.PropTypes.array.isRequired,
    selectedLimits: React.PropTypes.array.isRequired,
    currentLimits: React.PropTypes.array,
  },

  // getInitialState() {
  //     return {
  //     };
  // },
  componentWillMount() {
    store.dispatch(receiveUserLimits());
  },
  componentWillReceiveProps() {

  },

  onChange(currentLimits, index, event) {
    event.preventDefault();
    let body = this.props.selectedLimits[index];
    const copyCurrentLimits = currentLimits;
    if (event.target.className === 'time_period') {
      copyCurrentLimits.time_period = event.target.value;
      body = Object.assign({}, body, copyCurrentLimits);
    } else {
      copyCurrentLimits.value = event.target.value;
      body = Object.assign({}, body, copyCurrentLimits);
    }
    store.dispatch(fetchUserLimits(body));
  },

  submitForm(e) {
    e.preventDefault();
    const refs = this.refs;
    const data = [];
    for (let i = 0; i < 4; i++) {
      if (refs[`period_${i}`] === undefined) {
        refs[`period_${i}`] = { value: null };
      }
      data.push({
        type: refs[`type${i}`].value,
        value: refs[`select_${i}`].value,
        time_period: refs[`period_${i}`].value,
        user: refs[`user${i}`].value,
      });
    }
    request.post('/api/account/user-limits/')
      .type('json')
      .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
      .send(data)
      .end((err, res) => {
        if (res.status >= 400) {
          store.dispatch(addMessage({
            header: res.body.detail || 'Error Updating Limits',
            level: 'warning',
          }));
        }
        if (res.status === 200) {
          store.dispatch(addMessage({
            header: res.body.detail,
            level: 'success',
            ttl: 1500,
          }));
        }
      });
  },

  createSelectOptions(data) {
    return data.map(arrElem => {
      let value = arrElem[0];
      let text = arrElem[1];
      return <option value={value} key={arrElem}>{text}</option>;
    });
  },

  createComponents() {
    if (this.props.userLimits !== undefined) {
      return this.props.userLimits.map((element, index) => {
        const currLimits = this.props.currentLimits[index];
        const currentValue = currLimits.value;
        const selectedValue = this.props.selectedLimits[index];
        const idValue = `id_form-${index}-value`;
        const nameValue = `select_${index}`;
        const idPeriod = `id_form-${index}-time_period`;
        const namePeriod = `period_${index}`;
        const idType = `id_form-${index}-type`;
        const nameType = `type${index}`;
        const idUser = `id_form-${index}-user`;
        const nameUser = `user${index}`;
        let htmlBlock;

        if (element.time_period) {
          htmlBlock = (
            <div className="line" key={`line_${index}`}>
              <div className="selects_description">
                <div>
                  <span className="description_head">{pageText[index].boldText}</span>
                  <span>{pageText[index].text}</span>
                </div>
                <div>
                  <span className="current_value">Current Limit Set: </span>
                  <span className="current_value_text" id="curr_deposit_limit">{currentValue}</span>
                </div>
              </div>
              <div className="container-line-block">
                <div className="line-block">
                  <label><sup>MAXIMUM</sup></label>
                  <select id={idValue} name={nameValue} ref={nameValue} value={selectedValue.value}
                    onChange={this.onChange.bind(this, selectedValue, index)}
                  >
                    {this.createSelectOptions(element.value)}
                  </select>
                </div>
                <div className="line-block">
                  <label><sup>TIME PERIOD</sup></label>
                  <select className="time_period" id={idPeriod} name={namePeriod} ref={namePeriod}
                    value={selectedValue.time_period} onChange={this.onChange.bind(this, selectedValue, index)}
                  >
                    {this.createSelectOptions(element.time_period)}
                  </select>
                </div>
              </div>
              <input id={idType} name={nameType} type="hidden" value={currLimits.type} ref={nameType} />
              <input id={idUser} name={nameUser} type="hidden" value={currLimits.user} ref={nameUser} />
            </div>
          );
        } else {
          htmlBlock = (
            <div className="line" key={`line_alt_${index}`}>
              <div className="selects_description">
                <div>
                  <span className="description_head">{pageText[index].boldText}</span>
                  <span>{pageText[index].text}</span>
                </div>
                <div>
                  <span className="current_value">Current Limit Set: </span>
                  <span className="current_value_text" id="curr_deposit_limit">{currentValue}</span>
                </div>
              </div>
              <div className="container-line-block">
                <div className="line-block">
                  <label><sup>MAXIMUM</sup></label>
                  <select id={idValue} name={nameValue} ref={nameValue} value={selectedValue.value}
                    onChange={this.onChange.bind(this, selectedValue, index)}
                  >
                    {this.createSelectOptions(element.value)}
                  </select>
                </div>
              </div>
              <input id={idType} name={nameType} type="hidden" value={currLimits.type} ref={nameType} />
              <input id={nameUser} name={nameUser} type="hidden" value={currLimits.user} ref={nameUser} />
            </div>
          );
        }
        return htmlBlock;
      });
    }
  },

  render() {
    return (
      <div>
        <h2 className="text-center">SET PLAY LIMITS</h2>

        <header className="content-message content-message--info">
          <p className="content-message__description">
            Use the following form to set user limits on gameplay, deposits, and free limits.
            Once applied, MA residents will not be able to increase this limit for 90 days.
          </p>
        </header>

        <form action="" method="post" onSubmit={this.submitForm}>
          {this.createComponents()}

          <div className="button_container">
            <button type="submit">SUBMIT</button>
          </div>
        </form>
      </div>
    );
  },
});

const LimitsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Limits);

renderComponent(
  <Provider store={store}>
    <LimitsConnected />
  </Provider>, '#set_user_limits'
);
