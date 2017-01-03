import React from 'react';
import * as ReactRedux from 'react-redux';
import {bindActionCreators} from 'redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { addMessage } from '../../actions/message-actions.js';
import { receiveUserLimits } from '../../actions/user.js'
import { fetchUserLimits } from '../../actions/user.js'
const { Provider, connect } = ReactRedux;
import request from 'superagent';
import Cookies from 'js-cookie';
var pageText = [
    {
        boldText: "Deposit Limit: ",
        text: "Please select a deposit limit that you would like applied to your account."
    },
    {
        boldText: "Contest Entry Alert: ",
        text: "Please select the number of entries and period for which you'd like to be alerted."
    },
    {
        boldText: "Contest Entry Limit: ",
        text: "Please select a limit for the number of contests you may enter in a time period."
    },
    {
        boldText: "Contest Entry Limit: ",
        text: "Please select the appropriate contest entry fee."
    }
];

function mapStateToProps(state) {
  return {
      csrftoken: Cookies.get('csrftoken'),
      userLimits: state.user.userLimits,
      currentLimits: state.user.currentLimits
  };
}

function mapDispatchToProps(dispatch) {
    return {
        actions: bindActionCreators({
            addMessage,
            receiveUserLimits
        }, dispatch),
    };
}


const Limits = React.createClass({

    propTypes: {
        user: React.PropTypes.object.isRequired,
        actions: React.PropTypes.object.isRequired,
        userLimits: React.PropTypes.object.isRequired,
    },

    // getInitialState() {
    //     return {
    //     };
    // },

    componentWillReceiveProps(){

    },

    componentWillMount() {
        store.dispatch(receiveUserLimits());
    },

    onChange(currSelect, event){
        var body  = this.props.userLimits.map(object => {
            if(object.id == currSelect.id){
                if(event.target.className == 'time_period'){
                    currSelect.time_period = event.target.value;
                    return Object.assign({}, object, currSelect)
                } else {
                    currSelect.value = event.target.value;
                    return Object.assign({}, object, currSelect)
                }
            } else {
                return object
            }
        });
        store.dispatch(fetchUserLimits(body));
    },

    submitForm(e) {
        e.preventDefault();
        request.post('/limits/')
            .set({'X-CSRFToken': Cookies.get('csrftoken')})
            .send('csrfmiddlewaretoken='+ Cookies.get('csrftoken'))
            .send('form-TOTAL_FORMS='+this.refs['form-TOTAL_FORMS'].value)
            .send('form-INITIAL_FORMS='+ this.refs['form-INITIAL_FORMS'].value)
            .send('form-MIN_NUM_FORMS='+ this.refs['form-MIN_NUM_FORMS'].value)
            .send('form-MAX_NUM_FORMS='+ this.refs['form-MAX_NUM_FORMS'].value)
            .send('form-0-value='+ this.refs['form-0-value'].value)
            .send('form-0-time_period='+ this.refs['form-0-time_period'].value)
            .send('form-0-type='+ this.refs['form-0-type'].value)
            .send('form-0-user='+ this.refs['form-0-user'].value)
            .send('form-0-id='+ this.refs['form-0-id'].value)
            .send('form-1-value='+ this.refs['form-1-value'].value)
            .send('form-1-time_period='+ this.refs['form-1-time_period'].value)
            .send('form-1-type='+ this.refs['form-1-type'].value)
            .send('form-1-user='+ this.refs['form-1-user'].value)
            .send('form-1-id='+ this.refs['form-1-id'].value)
            .send('form-2-value='+ this.refs['form-2-value'].value)
            .send('form-2-time_period='+ this.refs['form-2-time_period'].value)
            .send('form-2-type='+ this.refs['form-2-type'].value)
            .send('form-2-user='+ this.refs['form-2-user'].value)
            .send('form-2-id='+ this.refs['form-2-id'].value)
            .send('form-3-value='+ this.refs['form-3-value'].value)
            .send('form-3-type='+ this.refs['form-3-type'].value)
            .send('form-3-user='+ this.refs['form-3-user'].value)
            .send('form-3-id='+ this.refs['form-3-id'].value)
            .end((err, res) => {
                if (err) {
                    store.dispatch(addMessage({
                        header: 'Request failed',
                        level: 'warning',
                    }))
                } if (res.status == 200){
                    store.dispatch(addMessage({
                        header: res.body.detail,
                        level: 'success',
                        ttl: 1500,
                    }))
                }
            });
    },

    createComponents(){
        if(this.props.userLimits != undefined){
            return this.props.userLimits.map( (element,index) => {
                let idValue = "id_form-"+index+"-value";
                let nameValue = "form-"+index+"-value";
                let idPeriod = "id_form-"+ index+"-time_period";
                let namePeriod = "form-"+index+"-time_period" ;
                let idType = "id_form-"+index+"-type";
                let nameType = "form-"+index+"-type";
                let idUser = "id_form-"+index+"-user";
                let nameUser = "form-"+index+"-user";
                let idId = "id_form-"+index+"-id";
                let nameId = "form-"+index+"-id";
                let currentValue = this.props.currentLimits[index].value;
                if(element.time_period){
                    return (
                        <div className="line">
                            <div className="selects_description">
                                <div>
                                    <span className="description_head">{pageText[index].boldText}</span>
                                <span
                                    id="">{pageText[index].text}</span>
                                </div>
                                <div>
                                    <span className="current_value">Current Limit Set: </span>
                                    <span className="current_value_text" id="curr_deposit_limit">{currentValue}</span>
                                </div>
                            </div>
                            <div className="container-line-block">
                                <div className="line-block">
                                    <label><sup>MAXIMUM</sup></label>
                                    <select id={idValue} name={nameValue} ref={nameValue} value={element.value} onChange={this.onChange.bind(this,element)}>
                                        <option value="50">$50</option>
                                        <option value="100">$100</option>
                                        <option value="250">$250</option>
                                        <option value="500">$500</option>
                                        <option value="750">$750</option>
                                        <option value="1000">$1000</option>
                                    </select>
                                </div>
                                <div className="line-block">
                                    <label><sup>TIME PERIOD</sup></label>
                                    <select className="time_period" id={idPeriod} name={namePeriod} ref={namePeriod} value={element.time_period} onChange={this.onChange.bind(this,element)}>
                                        <option value="30">Monthly</option>
                                        <option value="7">Weekly</option>
                                        <option value="1">Daily</option>
                                    </select>
                                </div>
                            </div>
                            <input id={idType} name={nameType} type="hidden" value={element.type} ref={nameType} />
                            <input id={idUser} name={nameUser} type="hidden" value={element.user} ref={nameUser} />
                            <input id={idId} name={nameId} type="hidden" value={element.id} ref={nameId} />
                        </div>
                    )
                } else {
                    return (
                        <div className="line">
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
                                    <select id={idValue} name={nameValue} ref={nameValue} value={element.value} onChange={this.onChange.bind(this,element)}>
                                        <option value="50" selected="selected">$50</option>
                                        <option value="100">$100</option>
                                        <option value="250">$250</option>
                                        <option value="500">$500</option>
                                        <option value="750">$750</option>
                                        <option value="1000">$1000</option>
                                    </select>
                                </div>
                            </div>
                            <input id={idType} name={nameType} type="hidden" value={element.type} ref={nameType}/>
                            <input id={idUser} name={nameUser} type="hidden" value={element.user} ref={nameUser}/>
                            <input id={idId} name={nameId} type="hidden" value={element.id} ref={nameId}/>
                        </div>
                    )
                }
            })
        }
    },

    render() {

        return (
            <div id="">
                <h2 className="text-center">
                    SET USER LIMITS
                </h2>

                <hr className="body-copy__h1-divider" />

                <div className="p_container">
                    <p>
                        Use the following form to set user limits on gameplay, deposits, and free limits.
                        Once applied, MA residents will not be able to increase this limit for 90 days.
                    </p>
                </div>

                <form action="" method="post" onSubmit={this.submitForm}>
                    <input id="id_form-TOTAL_FORMS" name="form-TOTAL_FORMS" type="hidden" value="4" ref="form-TOTAL_FORMS"/>
                    <input id="id_form-INITIAL_FORMS" name="form-INITIAL_FORMS" type="hidden" value="4" ref="form-INITIAL_FORMS" />
                    <input id="id_form-MIN_NUM_FORMS" name="form-MIN_NUM_FORMS" type="hidden" value="0" ref="form-MIN_NUM_FORMS"/>
                    <input id="id_form-MAX_NUM_FORMS" name="form-MAX_NUM_FORMS" type="hidden" value="4" ref="form-MAX_NUM_FORMS"/>
                    {this.createComponents()}
                    <div className="button_container">
                        <button type="submit">SUBMIT</button>
                    </div>
                </form>
            </div>
        )
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