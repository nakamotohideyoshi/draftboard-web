import React from 'react';
import FeaturedContests from '../../../components/contest-list/featured-contests.jsx';
import { expect } from 'chai';
import sd from 'skin-deep';


const props = {
  featuredContests: [
    {
      start_time: '2015-12-14T18:22:26Z',
      end_time: '2016-12-14T18:22:27Z',
      image_url: 'http://localhost:8080/static/src/img/temp/featured-contest.png',
      links_to: 'http://localhost:8080/lobby/5/',
    },
    {
      start_time: '2015-12-14T18:22:26Z',
      end_time: '2016-12-14T18:22:27Z',
      image_url: 'http://localhost:8080/static/src/img/temp/featured-contest.png',
      links_to: 'http://localhost:8080/lobby/5/',
    },
    {
      start_time: '2015-12-14T18:22:26Z',
      end_time: '2016-12-14T18:22:27Z',
      image_url: 'http://localhost:8080/static/src/img/temp/featured-contest.png',
      links_to: 'http://localhost:8080/lobby/5/',
    },
    {
      start_time: '2015-12-14T18:22:26Z',
      end_time: '2016-12-14T18:22:27Z',
      image_url: 'http://localhost:8080/static/src/img/temp/featured-contest.png',
      links_to: 'http://localhost:8080/lobby/5/',
    },
  ],
};

describe('FeaturedContests Component', () => {
  let vdom;
  let instance;

  beforeEach(() => {
    const tree = sd.shallowRender(React.createElement(FeaturedContests, props));
    instance = tree.getMountedInstance();
    vdom = tree.getRenderOutput();
  });


  it('should render a div for each contest', () => {
    // count up child 'div's
    const childDivs = vdom.props.children.filter(
      (child) => child.props.className === 'featured-contests--contest'
    );

    expect(vdom.type).to.equal('div');
    expect(childDivs.length).to.equal(props.featuredContests.length);
  });


  it('should render a link for each contest', () => {
    // count up child images
    const childLinks = vdom.props.children.filter(
      (child) => child.props.children.type === 'a'
    );

    expect(childLinks.length).to.equal(props.featuredContests.length);
  });


  it('should render an image for each contest', () => {
    // count up child images
    const childImgs = vdom.props.children.filter(
      (child) => child.props.children.props.children.type === 'img'
    );

    expect(childImgs.length).to.equal(props.featuredContests.length);
  });
});
