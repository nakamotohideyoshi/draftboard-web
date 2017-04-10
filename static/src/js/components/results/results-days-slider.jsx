import merge from 'lodash/merge';
import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import Slider from 'react-slick';
import { getDaysForMonth, weekdayNumToName } from '../../lib/time.js';
import { dateNow } from '../../lib/utils';

// assets
require('../../../sass/lib/slick-carousel.scss');


//const LeftNavButton = (props) => (<div {...props}>&lt;</div>);
//const RightNavButton = (props) => (<div {...props}>&gt;</div>);

const ResultsDaysSlider = React.createClass({

  propTypes: {
    year: React.PropTypes.number.isRequired,
    month: React.PropTypes.number.isRequired,
    day: React.PropTypes.number.isRequired,
    onSelectDate: React.PropTypes.func.isRequired,
  },

  mixins: [PureRenderMixin],


  getInitialState() {
    return {
      itemsList: this.getItemsList(),
      settings: {
        dots: false,
        infinite: false,
        // prevArrow: <LeftNavButton />,
        // nextArrow: <RightNavButton />,

        prevArrow: <this.getLeftButton />,
        nextArrow: <this.getRightButton />,
        speed: 500,
        initialSlide: this.props.day - 1,
        slidesToShow: 7,
        slidesToScroll: 7,
        variableWidth: true,
        afterChange: this.changeStateDate,
        beforeChange: this.beforeChangeStateDate
      },
      day: this.props.day,
      month: this.props.month,
      year: this.props.year,
    };
  },

  componentWillReceiveProps(nextProps) {
    const state = merge({}, this.state);

    state.itemsList = this.getItemsList();
    state.settings.initialSlide = nextProps.day - 1;
    this.setState(state);
    this.setState({
      day: this.props.day,
      month: this.props.month,
      year: this.props.year,
    });
    this.refs.slider.slickGoTo(nextProps.day - 1);
  },

  getRightButton(props){
    return (<div {...props} onClick={this.nextSlide.bind(this,props.className)}>&gt;</div>)
  },
  getLeftButton(props){
    return (<div {...props} onClick={this.prevSlide.bind(this,props.className)}>&lt;</div>)
  },

  nextSlide(className) {
    let week = 7;
    if(new RegExp('slick-disabled').test(className)){
      let today = new Date().getTime();
      let calendarDate = new Date( this.state.year,this.state.month ,this.state.day + week).getTime();
      if(calendarDate < today){
        //Set the first day of next month
        if( (this.props.month + 1) > 12 ){
          this.props.onSelectDate(this.props.year + 1 , 1 , 1);
        } else {
          this.props.onSelectDate(this.props.year, this.props.month + 1, 1);
        }
      }
    } else {
      this.refs.slider.slickNext();
    }
  },

  prevSlide(className) {
    if (new RegExp('slick-disabled').test(className)) {
      if (!(this.props.month - 1)) {
        let date = new Date(this.props.year - 1 , 11);
        let dayOfMonth = date.getDate();
        date.setDate(dayOfMonth - 1);
        let lastDay = date.getDate();
        this.props.onSelectDate(this.props.year - 1, 12 , lastDay);
      } else {
        let date = new Date(this.props.year , this.props.month - 1);
        let dayOfMonth = date.getDate();
        date.setDate(dayOfMonth - 1);
        let lastDay = date.getDate();
        this.props.onSelectDate(this.props.year, this.props.month - 1, lastDay);
      }
    } else {
      this.refs.slider.slickPrev();
    }
  },

  changeStateDate(){
    let day;
    if(this.state.isRightArrow){
      day = this.state.day + 7
    } else {
      day = this.state.day - 7
    }
    this.setState({
      day: day
    });
  },

  beforeChangeStateDate(prevSlide,nextSlide){
    console.log('prevSlide', prevSlide,'nextSlide', nextSlide);
  },

  getItemsList() {
    const mapDay = (d, index) => {
      const selected = d.getDate() === this.props.day && d.getMonth() === this.props.month - 1;

      const foo = {
        id: d.toString(),
        index,
        daynum: d.getDate(),
        weekday: weekdayNumToName(d.getDay() === 0 ? 6 : d.getDay() - 1),
        selected,
      };

      return foo;
    };

    return getDaysForMonth(this.props.year, this.props.month).map(mapDay);
  },

  getItems() {
    return this.state.itemsList.map(i => {
      const itemTime = (new Date(
        this.props.year,
        this.props.month - 1,
        i.daynum
      )).getTime();
      const isInTheFuture = itemTime > dateNow();

      let className = 'item';
      if (i.selected) className += ' selected';
      if (isInTheFuture) className += ' future';

      return [
        <div key={i.id}
          className={className}
          onClick={isInTheFuture ? null : this.handleSelectDate.bind(this, i.daynum)}
        >
          {i.weekday}
          <span className="value">{i.daynum}</span>
          <div className="separator"><span /></div>
        </div>,
      ];
    }).reduce(
      // Just flatten the array on a single level. Not using lodash here,
      // because this may result in unexpected behavior depending on the
      // rendered React component internal representation.
      (accum, l) => accum.concat.apply(accum, l), []
    );
  },

  // changeHandler() {
  //   // -1 for index vs day
  //   this.refs.slider.slickGoTo(this.props.day - 1);
  // },

  handleSelectDate(day) {
    this.props.onSelectDate(this.props.year, this.props.month, day);
  },

  render() {
    return (
      <div className="results-days-slider">
        <Slider ref="slider" {...this.state.settings}>
          {this.getItems()}
        </Slider>
      </div>
    );
  },

});


export default ResultsDaysSlider;
