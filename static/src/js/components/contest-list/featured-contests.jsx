import React from 'react'


/**
 * A list of featured contest banners in the lobby. These get created in the admin section.
 */
var FeaturedContests = React.createClass({
  propTypes: {
    featuredContests: React.PropTypes.array.isRequired
  },


  getFeaturedContests: function() {
    if (!this.props.featuredContests) {
      return ('')
    }

    return this.props.featuredContests.map(function(contest) {
      return (
        <div className="featured-contests--contest" key={contest.image_url}>
          <a href={contest.links_to}>
            <img src={contest.image_url} />
          </a>
        </div>
      )
    })
  },


  render: function() {
    return (
      <div>
        {this.getFeaturedContests()}
      </div>
    )
  }

})

module.exports = FeaturedContests
