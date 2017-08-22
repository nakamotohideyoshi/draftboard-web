import NBAPlayRecapVO from './nba/NBAPlayRecapVO';
import NBAPlayAnimation from './nba/PlayAnimation';
import NBACourt from './nba/NBACourt';
import NFLLiveAnimationFactory from './nfl/NFLLiveAnimationFactory';

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
        return animation.play(recap, stage);
      case 'nfl':
        return (new NFLLiveAnimationFactory()).play(data, element);
      default:
        throw new Error(`Unable to create LiveAnimation for unsupported sport ${data.sport}`);
    }
  }
}
