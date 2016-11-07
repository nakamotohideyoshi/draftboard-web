import merge from 'lodash/merge';
import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import Slider from 'react-slick';
import { LiveBigPlay } from './live-big-play';

// assets
require('../../../sass/lib/slick-carousel.scss');
require('../../../sass/blocks/live/live-big-plays.scss');


const LeftNavButton = (props) => (<div {...props}>&lt;</div>);
const RightNavButton = (props) => (<div {...props}>&gt;</div>);

export const LiveBigPlays = React.createClass({

  propTypes: {
    queue: React.PropTypes.array.isRequired,
  },

  mixins: [PureRenderMixin],

  getInitialState() {
    return {
      settings: {
        dots: false,
        infinite: false,
        prevArrow: <LeftNavButton />,
        nextArrow: <RightNavButton />,
        speed: 500,
        initialSlide: 1,
        slidesToShow: 4,
        slidesToScroll: 4,
        rtl: true,
      },
    };
  },

  componentDidMount() {
    window.addEventListener('resize', this.handleResize);

    this.handleResize();
  },

  componentWillReceiveProps(nextProps) {
    const state = merge({}, this.state);

    state.settings.initialSlide = nextProps.queue.length - 1;
    this.setState(state);

    this.refs.bigPlaysSlider.slickGoTo(state.settings.initialSlide);
  },

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },

  handleResize() {
    const windowWidth = window.innerWidth;
    const state = merge({}, this.state);

    if (windowWidth < 1140) {
      state.settings.slidesToShow = 3;
      state.settings.slidesToScroll = 3;
    }
    if (windowWidth >= 1140) {
      state.settings.slidesToShow = 4;
      state.settings.slidesToScroll = 4;
    }

    this.setState(state);
  },

  // weird bug with react-slick means you have to wrap each child in a div
  // https://github.com/akiran/react-slick/issues/328#issuecomment-230662664
  render() {
    return (
      <div className="live-big-plays">
        <Slider ref="bigPlaysSlider" {...this.state.settings}>
          {this.props.queue.map((i) => (
            <div key={i.id}><LiveBigPlay event={i} /></div>
          ))}
        </Slider>
      </div>
    );
  },

});

export default LiveBigPlays;
