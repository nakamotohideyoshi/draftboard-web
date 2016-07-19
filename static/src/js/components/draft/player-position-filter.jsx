import React from 'react';
import CollectionMatchFilter from '../filters/collection-match-filter.jsx';
import find from 'lodash/find';
import log from '../../lib/logging.js';


/**
 * A wrapper around CollectionMatchFilter that will auto-select the filter that matches the
 * first empty roster slot in a lineup that is being created.
 *
 * This means that when you first hit the draft page, the top roster slot position will be
 * pre-filtered, once that slot is filled, the next position filter is applied.
 */
const PlayerPositionFilter = React.createClass({
  propTypes: {
    handleFilterChange: React.PropTypes.func.isRequired,
    positions: React.PropTypes.array,
    newLineup: React.PropTypes.array,
    activeFilter: React.PropTypes.object,
  },


  componentWillMount() {
    this.selectNextRosterSlotFilter(this.props.newLineup);
  },


  componentWillReceiveProps(nextProps) {
    // If the filter was NOT changed by user-interaction, automatically find the
    // next valid filter based on the lineup that is being created.
    if (nextProps.activeFilter === this.props.activeFilter) {
      this.selectNextRosterSlotFilter(nextProps.newLineup);
    }
  },


  selectNextRosterSlotFilter(lineup) {
    const nextSlot = find(lineup, (slot) => !slot.player);

    if (nextSlot) {
      const autoActiveFilter = find(this.props.positions, { title: nextSlot.name });

      if (autoActiveFilter) {
        if (this.props.activeFilter && autoActiveFilter.match !== this.props.activeFilter.match) {
          this.props.handleFilterChange(
            'positionFilter',
            autoActiveFilter.column,
            autoActiveFilter.match
          );
        }
      }
    } else {
      log.trace('no matching filter found to auto-select.');
    }
  },


  render() {
    // If we have a list of positions, the first one will be the initial position
    // that is filtered.
    let initialFilterMatch = '';
    // The first one is "all" so we ignore the [0] index.
    if (this.props.positions.length >= 2) {
      initialFilterMatch = this.props.positions[1].match;
    }

    return (
      <div className="cmp-player-position-filter">
        <CollectionMatchFilter
          className="collection-filter--player-type"
          filters={this.props.positions}
          filterName="positionFilter"
          filterProperty="position"
          match={initialFilterMatch}
          onUpdate={this.props.handleFilterChange}
          activeFilter={this.props.activeFilter}
        />
      </div>
    );
  },
});


module.exports = PlayerPositionFilter;
