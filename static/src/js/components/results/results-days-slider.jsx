import merge from 'lodash/merge';
import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import Slider from 'react-slick';
import { getDaysForMonth, weekdayNumToName } from '../../lib/time.js';
import { dateNow } from '../../lib/utils';

// assets
require('../../../sass/lib/slick-carousel.scss');


// const LeftNavButton = (props) => (<div {...props}>&lt;</div>);
// const RightNavButton = (props) => (<div {...props}>&gt;</div>);

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
        afterChange: this.afterChangeHandler,
      },
    };
  },

  componentWillReceiveProps(nextProps) {
    const state = merge({}, this.state);
    // Forced overwrite properties before getting the new items;
    this.props.day = nextProps.day;
    this.props.month = nextProps.month;
    this.props.year = nextProps.year;
    state.itemsList = this.getItemsList();
    state.settings.initialSlide = nextProps.day - 1;
    this.setState(state);
  },

  componentDidUpdate() {
    // Sliding only after updating of all properties
    this.refs.slider.slickGoTo(this.props.day - 1);
  },

  getRightButton(props) {
    return (<div {...props} onClick={this.nextSlide.bind(this, props.className)}>&gt;</div>);
  },
  getLeftButton(props) {
    return (<div {...props} onClick={this.prevSlide.bind(this, props.className)}>&lt;</div>);
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

  afterChangeHandler(currSlide) {
    const today = dateNow();
    const future = new Date(this.props.year, this.props.month - 1, currSlide + 1).getTime();
    if (today > future) {
      this.props.onSelectDate(this.props.year, this.props.month, currSlide + 1);
    } else {
      // we don't change anything
      return false;
    }
  },

  prevSlide(className) {
    if (new RegExp('slick-disabled').test(className)) {
      if (!(this.props.month - 1)) {
        const date = new Date(this.props.year - 1, 12);
        const dayOfMonth = date.getDate();
        date.setDate(dayOfMonth - 1);
        const lastDay = date.getDate();
        this.props.onSelectDate(this.props.year - 1, 12, lastDay);
      } else {
        const date = new Date(this.props.year, this.props.month - 1);
        const dayOfMonth = date.getDate();
        date.setDate(dayOfMonth - 1);
        const lastDay = date.getDate();
        this.props.onSelectDate(this.props.year, this.props.month - 1, lastDay);
      }
    } else {
      this.refs.slider.slickPrev();
    }
  },

  nextSlide(className) {
    const week = 7;
    if (new RegExp('slick-disabled').test(className)) {
      const today = dateNow();
      const sliderDate = new Date(this.props.year, this.props.month - 1, this.props.day + week).getTime();
      const isPast = sliderDate < today;
      if (isPast) {
        if ((this.props.month + 1) > 12) {
          this.props.onSelectDate(this.props.year + 1, 1, 1);
        } else {
          // The next line is the solution to the problem when the number of elements for the slider
          // becomes smaller than the index of the current slide
          this.refs.slider.innerSlider.setState({
            currentSlide: 0,
          });
          this.props.onSelectDate(this.props.year, this.props.month + 1, 1);
        }
      }
    } else {
      this.refs.slider.slickNext();
    }
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
