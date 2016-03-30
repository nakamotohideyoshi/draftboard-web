import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import MessageDisplayMessage from '../../../components/site/message-display-message.jsx';

const defaultTestProps = {
  message: {
    level: 'theMessageLevel',
    header: 'theMessageHeader',
    content: 'theMessageContent',
  },
  messageId: '666abc',
  removeMessage: () => true,
};


describe('<MessageDisplayMessage /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<MessageDisplayMessage {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render the message and close button.', () => {
    expect(wrapper.find('.message')).to.have.length(1);
    expect(wrapper.find('.btn-close')).to.have.length(1);
  });
});
