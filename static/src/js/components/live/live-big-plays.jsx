import merge from 'lodash/merge';
import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import Slider from 'react-slick';
import { humanizeFP } from '../../lib/utils/numbers';
import cleanDescription from '../../lib/utils/nfl-clean-pbp-description';

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
    const itemsList = this.getItems();

    return {
      itemsList,
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

  componentWillReceiveProps() {
    const state = merge({}, this.state);

    state.itemsList = this.getItems();
    state.settings.initialSlide = state.itemsList - 1;
    this.setState(state);

    this.refs.bigPlaysSlider.slickGoTo(state.settings.initialSlide);
  },

  componentWillUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },

  getItems() {
    const items = [];

    this.props.queue.map(i => {
      const block = 'live-big-plays__play';
      const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${i.sport}`;
      const { description, winning, eventPlayers, playerFPChanges, homeScoreStr, awayScoreStr, when } = i;
      const cleanedDescription = cleanDescription(description);

      if (i.eventPlayers.length === 1) {
        const playerId = eventPlayers[0];
        const classNames = `${block} ${block}--1-players`;

        items.push(
          <div
            key={`${i.id}-${new Date().getTime()}`}
            className={classNames}
          >
            <div className={`${block}__inner`}>
              <img
                className={`${block}__player-photo`}
                src={`${playerImagesBaseUrl}/120/${playerId}.png`}
                alt=""
              />
              <div className={`${block}__description`}>
                <div className={`${block}__description-content`}>
                  {cleanedDescription}
                </div>
              </div>
              <div className={`${block}__player-points`}>
                {humanizeFP(playerFPChanges[playerId] || 0, true)}
              </div>
              <div className={`${block}__game`}>
                <div className={`${block}__score ${block}__${winning}-winning`}>
                  <div className={`${block}__home-team`}>
                    {homeScoreStr}
                  </div>
                  &nbsp;-&nbsp;
                  <div className={`${block}__away-team`}>
                    {awayScoreStr}
                  </div>
                </div>
                <div className={`${block}__when`}>
                  Q{when.quarter} {when.clock}
                </div>
              </div>
            </div>
          </div>
        );
      }

      // different template, maybe combine these in the future?
      if (i.eventPlayers.length === 2) {
        const classNames = `${block} ${block}--2-players`;

        const players = i.eventPlayers.map(playerId => (
          <li
            key={playerId}
            className={`${block}__player`}
          >
            <div className={`${block}__player-points`}>
              {humanizeFP(playerFPChanges[playerId] || 0, true)}
            </div>
            <img
              className={`${block}__player-photo`}
              src={`${playerImagesBaseUrl}/120/${playerId}.png`}
              alt=""
            />
          </li>
        ));

        items.push(
          <div
            key={i}
            className={classNames}
          >
            <div className={`${block}__inner`}>
              <div className={`${block}__description`}>
                <div className={`${block}__description-content`}>
                  {cleanedDescription}
                </div>
              </div>
              <ul className={`${block}__players`}>
                {players}
              </ul>
              <div className={`${block}__game`}>
                <div className={`${block}__score ${block}__${winning}-winning`}>
                  <div className={`${block}__home-team`}>
                    {homeScoreStr}
                  </div>
                  &nbsp;-&nbsp;
                  <div className={`${block}__away-team`}>
                    {awayScoreStr}
                  </div>
                </div>
                <div className={`${block}__when`}>
                  Q{when.quarter} {when.clock}
                </div>
              </div>
            </div>
          </div>
        );
      }
    });

    return items;
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

  render() {
    return (
      <div className="live-big-plays">
        <Slider ref="bigPlaysSlider" {...this.state.settings}>
          {this.getItems()}
        </Slider>
      </div>
    );
  },

});

export default LiveBigPlays;
