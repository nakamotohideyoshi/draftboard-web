"use strict";

var Reflux = require("reflux");
// var ContestActions = require("../actions/contest-actions");
var request = require("superagent");
var log = require("../lib/logging");
var FilterableMixin = require('./mixins/filterable-mixin.js');
var SortableMixin = require('./mixins/sortable-mixin');
var _find = require('lodash/collection/find');


var ContestStore = Reflux.createStore({
  mixins: [
    FilterableMixin,
    SortableMixin
  ],
  data: {},
  filters: [],
  allContests: [],

  init: function() {
    log.debug('ContestStore.init()');
    this.resetState();

    // this.listenTo(ContestActions.load, this.fetchContests);
    // this.listenTo(ContestActions.contestFocused, this.setFocusedContest);
    // this.listenTo(ContestActions.registerFilter, this.registerFilter);
    // this.listenTo(ContestActions.filterUpdated, this.filterUpdated);
    // this.listenTo(ContestActions.clearFilters, this.clearFilters);
    // this.listenTo(ContestActions.setSortProperty, this.setSortProperty);
    // this.listenTo(ContestActions.setSortDirection, this.setSortDirection);

    this.fetchContests();
  },


  resetState: function() {
    this.filters = [];
    this.allContests = [];
    this.data = {
      filteredContests: {},
      focusedContestId: null,
      sortKey: 'id',
      sortDirection: 'asc',
      activeFilters: []
    };
  },


  /**
   * Get a list of contests from the data source.
   */
  fetchContests: function() {
    var self = this;
    request
      .get("/contest/lobby/")
      .set({'X-REQUESTED-WITH':  'XMLHttpRequest'})
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          log.error(err);
          // ContestActions.load.failed(err);
        } else {
          self.allContests = res.body.results;
          self.data.filteredContests = res.body.results;
          // ContestActions.load.completed();
          self.trigger(self.data);
        }
    });
  },


  /**
   * Return the focused contest.
   * @return {Object} the focused contest.
   */
  getFocusedContest: function() {
    return _find(this.allContests, 'id', this.data.focusedContestId);
  },


  /**
   * Set the focused contest based on the provided contest ID.
   * @param {number} contestId the ID of the contest to set as active.
   */
  setFocusedContest: function(contestId) {
    if(typeof contestId === 'number') {
      this.data.focusedContestId = contestId;
      this.trigger(this.data);
    }
  },


  /**
   * Return the next visible row.
   * @return {[type]} [description]
   */
  getNextVisibleRowId: function() {
    var currentlyActiveIndex = this.getCurrentfocusedContestIndex();

    // If there are no contests, return immediately.
    if(this.data.filteredContests.length === 0) {
      log.warn('There are no contests.');
      return null;
    }

    // If there isn't a currently active contest, return the first row.
    if(currentlyActiveIndex === null) {
      log.debug('No current contest, activating the first one.');
      return this.data.filteredContests[0].id;
    }

    // If there is a current contest, return the next one, if one exists.
    if(currentlyActiveIndex + 1 < this.data.filteredContests.length) {
      return this.data.filteredContests[currentlyActiveIndex + 1].id;
    } else {
      log.warn('The last contest has focus, there is no next.');
      return null;
    }
  },


  /**
   * Return the previous visible row.
   * @return {[type]} [description]
   */
  getPreviousVisibleRowId: function() {
    var currentlyActiveIndex = this.getCurrentfocusedContestIndex();

    // If there are no contests, return immediately.
    if(this.data.filteredContests.length === 0) {
      log.warn('There are no contests.');
      return null;
    }

    // If there isn't a currently active contest, return the first row.
    if(currentlyActiveIndex === null) {
      log.debug('No current contest, activating the first one.');
      return this.data.filteredContests[0].id;
    }

    // If we're not already on the first contest, go to the previous.
    if(currentlyActiveIndex !== 0) {
      return this.data.filteredContests[currentlyActiveIndex - 1].id;
    } else {
      log.warn('There is no previous contest.');
      return null;
    }
  },


  /**
   * We know the ID of the focused contest, this will figure out the index of the element in the
   * filteredContests array.
   *
   * @return {number} the index of the contest in the list.
   */
  getCurrentfocusedContestIndex: function() {
    // If there aren't any visible contests, nope!
    if(this.data.filteredContests.length === 0) {
      return null;
    }

    // Loop through and find it in the list.
    for (var i = 0; i < this.data.filteredContests.length; i++) {
      if (this.data.focusedContestId === this.data.filteredContests[i].id) {
        return i;
      }
    }

    // If we didn't find it in the list, nope again!.
    return null;
  },


  sortableUpdated: function() {
    this.data.filteredContests = this.sort(this.data.filteredContests);
    this.trigger(this.data);
  },


  /**
   * A hook for filters to notify us that one of the filters has changed and this
   * store needs to re-filter the data.
   *
   * @param {string} filterName - The name of the filter component.
   */
  filterUpdated: function(filterName, filter) {
    log.debug('ContestStore.filterUpdated() - ' + filterName, filter);
    this.data.activeFilters[filterName] = filter;
    // When a filter is updated, update our stored display rows.
    this.data.filteredContests = this.runFilters(this.allContests);
    this.data.filteredPlayers = this.sort(this.data.filteredPlayers);
    this.trigger(this.data);
  }

});


module.exports = ContestStore;
