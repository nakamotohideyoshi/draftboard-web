"use strict";

var Reflux = require("reflux");
var DraftActions = require("../actions/draft-actions");
var request = require("superagent");
var log = require("../lib/logging");
var FilterableMixin = require('./mixins/filterable-mixin.js');
var SortableMixin = require('./mixins/sortable-mixin.js');


/**
 * Store a DraftGroup (players for a specific set of contests).
 */
var DraftGroupStore = Reflux.createStore({

  mixins: [FilterableMixin, SortableMixin],
  data: {},
  filters: [],
  allPlayers: [],
  // Default sort to descending salaries.
  sortProperty: 'salary',
  sortDirection: 'desc',


  init: function() {
    this.listenTo(DraftActions.loadDraftGroup, this.fetchDraftGroup);
    this.listenTo(DraftActions.registerFilter, this.registerFilter);
    this.listenTo(DraftActions.filterUpdated, this.filterUpdated);
    this.listenTo(DraftActions.setSortProperty, this.setSortProperty);
    this.listenTo(DraftActions.setSortDirection, this.setSortDirection);

    this.data = {
      draftGroupId: null,
      filteredPlayers: [],
      sport: null,
      activeFilters: []
    };
  },


  /**
   * Get a list of the user's lineups from the data source.
   */
  fetchDraftGroup: function(draftGroupId) {
    log.debug('DraftGroupStore.fetchDraftGroup()', draftGroupId);

    // Nope outta here if there wasn't an id provided.
    if (!draftGroupId) {
      log.error('fetchDraftGroup() - No draftGroupId specified.');
      DraftActions.loadDraftGroup.failed('fetchDraftGroup() - No draftGroupId specified.');
      return;
    }

    request
      .get("/draft-group/" + draftGroupId + '/')
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          // Fail the action's promise.
          log.error(err);
          DraftActions.loadDraftGroup.failed(err);
        } else {
          this.data.draftGroupId = draftGroupId;
          this.newDataFetched(res.body);
          // Complete the action's promise.
          DraftActions.loadDraftGroup.completed();
        }
    }.bind(this));
  },


  newDataFetched: function(payload) {
    log.debug('DraftGroupStore.newDataReceived()');

    // Update the store with our new data.
    this.data.sport = payload.sport;
    this.allPlayers = payload.players;
    this.data.filteredPlayers = this.sort(payload.players);

    // Trigger a data flow.
    this.trigger(this.data);
  },


  sortableUpdated: function() {
    this.data.filteredPlayers = this.sort(this.data.filteredPlayers);
    this.trigger(this.data);
  },


  /**
   * A hook for filters to notify us that one of the filters has changed and this
   * store needs to re-filter the data.
   *
   * @param {string} filterName - The name of the filter component.
   */
  filterUpdated: function(filterName, filter) {
    log.debug('DraftGroupStore.filterUpdated() - ' + filterName, filter);
    this.data.activeFilters[filterName] = filter;
    // When a filter is updated, update our stored display rows.
    this.data.filteredPlayers = this.runFilters(this.allPlayers);
    this.data.filteredPlayers = this.sort(this.data.filteredPlayers);
    this.trigger(this.data);
  }

});


module.exports = DraftGroupStore;
