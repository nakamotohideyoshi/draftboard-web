import NBAPlayRecapVO from './nba/NBAPlayRecapVO';
import NBAPlayAnimation from './nba/PlayAnimation';
import NBACourt from './nba/NBACourt';
import NFLPlayRecapVO from './nfl/NFLPlayRecapVO';
import NFLField from './nfl/NFLField';
import NFLLivePlayAnimation from './nfl/NFLLivePlayAnimation';

export default class LiveAnimationFactory {

  play(data, element) {
    let recap;
    let stage;
    let animation;

    if (!data.hasOwnProperty('sport')) {
      throw new Error('Unable to create LiveAnimation for unknown sport.');
    }

    switch (data.sport) {
      case 'nba':
        recap = new NBAPlayRecapVO(data);
        stage = new NBACourt(element);
        animation = new NBAPlayAnimation();
        break;
      case 'nfl':
        recap = new NFLPlayRecapVO(data);
        stage = new NFLField(element);
        animation = new NFLLivePlayAnimation();
        break;
      default:
        throw new Error(`Unable to create LiveAnimation for unsupported sport ${data.sport}`);
    }

    if (window.debug_live_animations_which_side) {
      recap._obj.whichSide = window.debug_live_animations_which_side;
    }

    return animation.play(recap, stage);
  }
}
