import React from 'react';


/**
 * A list of featured contest banners in the lobby. These get created in the admin section.
 */
const FeaturedContests = React.createClass({
  propTypes: {
    featuredContests: React.PropTypes.array.isRequired,
  },


  getFeaturedContests() {
    if (!this.props.featuredContests) {
      return ('');
    }

    return this.props.featuredContests.map((contest) => (
        <div className="featured-contests--contest" key={contest.image_url}>
          <a href={contest.links_to} target="_blank">
            <img
              alt="Featured Contest Banner"
              src={contest.image_url}
            />
          </a>
        </div>
      )
    );
  },


  render() {
    return (
      <div>
        {this.getFeaturedContests()}
      </div>
    );
  },

});


module.exports = FeaturedContests;
