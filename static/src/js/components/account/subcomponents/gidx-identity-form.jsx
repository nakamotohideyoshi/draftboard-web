import React from 'react';

window.gidxServiceSettings = function () {
  console.log('========= gidxServiceSettings =========');
  window.gidxBuildSteps = true;
  // this is the dom object (div) where the cashier/registration service should be embedded on the page.
  window.gidxContainer = '#GIDX_ServiceContainer';
};

window.gidxErrorReport = function (error, errorMsg) {
  console.log('======= gidxErrorReport =========');
  console.error(error, errorMsg);
  // Error messages will be sent here by the GIDX Client Side Service
};

window.gidxNextStep = function () {
    console.log('========= gidxNextStep ===========');

  // Once the customer has completed this Session the GIDX Client Side Service will call this function.
  //  You should now make an "aJax" call or do a "document.location='a page on your server'" and call
  // the the appropriate API Method.
};


const GidxIdentityForm = React.createClass({
  propTypes: {
    embed: React.PropTypes.string.isRequired,
  },


  getInitialState() {
    return {
      status: 'NONE',
    };
  },


  componentDidMount() {
    const self = this;

    window.gidxServiceStatus = function (service, action, json) {
      // service idAcctComplete-plate == process over.
      if (service === 'idAcctComplete-plate') {
        self.setState({ status: 'COMPLETE__FAIL' });
      }

      console.log('========= gidxServiceStatus ============');

      console.log('service', service);
      console.log('action', action);
      console.log('json', json);

      // during each "step" within a Web Session process this function is called by the GIDX Client Side Service
      // providing you the service action that was just performed, the start & stop time, and a JSON key/value
      // that you can parse/loop to get more data control of the process.
      // Here's an example of getting the deposit value selected and displaying it within an element on the page.
      for (var i = 0; i < json.length; i++) {
        for (var key in json[i]) {
          if (json[i].hasOwnProperty(key)) {
          // Here you can look at the key and value to make decisions on what you would
          // like to do with the client side interface.
          var sItem = key;
          var sValue = json[i][key];
            console.log(sItem + ': ', sValue);
            // Example
            if (sItem === 'TransactionAmount') {
              document.getElementById('DepositAmountDisplay').innerText(sValue);
            }
          }
        }
      }
    };


    // This is some hack-ass shit.
    const scriptTag = document.querySelector('#GIDX script');
    const newScriptTag = document.createElement('script');

    newScriptTag.type = 'text/javascript';
    newScriptTag.src = scriptTag.src;

    for (let i = 0; i < scriptTag.attributes.length; i++) {
      const a = scriptTag.attributes[i];
      newScriptTag.setAttribute(a.name, a.value);
    }
    this.refs.originalEmbed.remove();
    this.refs.GIDX_embed.append(newScriptTag);
  },


  shouldComponentUpdate(nextProps, nextState) {
    // Only re-render if we set new state, not for passed props.
    return this.state !== nextState;
  },


  render() {

    if (this.state.status === 'COMPLETE__FAIL') {
      return (
        <div>
          <h3>Unable Verify Your Identity</h3>
          <p>Please contact support@draftboard.com with any questions.</p>
        </div>
      );
    }

    return (
      <div>
        <div id="DepositAmountDisplay"></div>
        <div id="GIDX_ServiceContainer"></div>


        <div id="GIDX">

          <div ref="GIDX_embed">
            <div data-gidx-script-loading='true'>Loading...</div>

            <div
              id="GIDX_embed_hidden"
              ref="originalEmbed"
              dangerouslySetInnerHTML={{__html: this.props.embed}}
            ></div>
          </div>

        </div>
      </div>
    );
  },
});


export default GidxIdentityForm;
