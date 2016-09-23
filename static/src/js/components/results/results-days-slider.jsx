import merge from 'lodash/merge';
import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import Slider from 'react-slick';
import { getDaysForMonth, weekdayNumToName } from '../../lib/time.js';
import { dateNow } from '../../lib/utils';

// assets
require('../../../sass/lib/slick-carousel.scss');


const LeftNavButton = (props) => (<div {...props}>&lt;</div>);
const RightNavButton = (props) => (<div {...props}>&gt;</div>);

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
        prevArrow: <LeftNavButton />,
        nextArrow: <RightNavButton />,
        speed: 500,
        initialSlide: this.props.day - 1,
        slidesToShow: 7,
        slidesToScroll: 7,
        variableWidth: true,
      },
    };
  },

  componentWillReceiveProps(nextProps) {
    const state = merge({}, this.state);

    state.itemsList = this.getItemsList();
    state.settings.initialSlide = nextProps.day - 1;
    this.setState(state);

    // if new month, trigger slick to change position
    if (this.props.month === nextProps.month) {
      this.refs.slider.slickGoTo(this.props.day - 1);
    }
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
