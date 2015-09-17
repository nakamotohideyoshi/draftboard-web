"use strict";

var Reflux = require("reflux");
var ContestActions = require("../actions/contest-actions");
var request = require("superagent");
var log = require("../lib/logging");
var _sortByOrder = require("lodash/collection/sortByOrder");


var ContestStore = Reflux.createStore({
  data: {},
  filters: [],

  init: function() {
    this.listenTo(ContestActions.load, this.fetchContests);
    this.listenTo(ContestActions.contestFocused, this.setFocusedContest);
    this.listenTo(ContestActions.registerFilter, this.registerFilter);
    this.listenTo(ContestActions.filterUpdated, this.filterUpdated);
    this.listenTo(ContestActions.clearFilters, this.clearFilters);
    this.listenTo(ContestActions.sortByKey, this.sortByKey);

    this.data = {
      filteredContests: {},
      contests: {},
      focusedContestId: null,
      sortKey: 'id',
      sortDirection: 'asc',
      activeFilters: []
    };

    this.fetchContests();
  },


  /**
   * Get a list of contests from the data source.
   */
  fetchContests: function() {
    var self = this;
    request
      .get("/contest/lobby/")
      .set('Accept', 'application/json')
      .end(function(err, res) {
        if(err) {
          log.error(err);
          ContestActions.load.failed(err);
        } else {
          self.data.contests = res.body.results;
          self.data.filteredContests = res.body.results;
          ContestActions.load.completed();
          self.trigger(self.data);
        }
    });
  },


  /**
   * Return the focused contest.
   * @return {Object} the focused contest.
   */
  getFocusedContest: function() {
    return this.data.contests[this.data.focusedContestId];
  },

  /**
   * Return the focused contest's id attribute.
   * @return {Object} the focused contest.
   */
  // getFocusedContestId: function() {
  //   if (this.data.contests[this.data.focusedContestId]) {
  //     return this.data.focusedContestId;
  //   } else {
  //     return null;
  //   }
  // },


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
   * Populate data.filteredContests with all of the contests that should be visible based on
   * any active filters.
   */
  filterContests: function() {
    var rows = [];
    // Loop through all sorted data rows, determine if they should be displayed and build a list
    // of visible data rows,
    for (var i = 0; i < this.data.contests.length; i++) {
      if(this.shouldDisplayRow(this.data.contests[i])) {
        rows.push(this.data.contests[i]);
      }
    }

    // Sort the rows by the currently active filter.
    if (this.data.sortDirection === 'desc') {
      rows = _sortByOrder(rows, this.data.sortKey).reverse();
    } else {
      rows = _sortByOrder(rows, this.data.sortKey);
    }

    this.data.filteredContests = rows;

    // this.data.filteredContests;
    this.trigger(this.data);
  },


  /**
   * Determine if a row should be dislayed by running the filter() method on all of
   * the component's registered filters.
   *
   * @param {Object} row - A row of data from the state.data array.
   * @return {boolean} Should the row be displayed?
   */
  shouldDisplayRow: function(row) {
    // Default to showing the row.
    var show = true;

    // Run through each registered filter and determine if the row should be displayed.
    for (var i in this.filters) {
      show = this.filters[i].filter(row);
      // As soon as we get a false, stop running filters and return;
      if (show === false) {
        break;
      }
    }

    return show;
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


  /**
   * Register a filter with this component.
   *
   * @param {Object} filterComponent - The react filter comonent.
   */
  registerFilter: function(filterComponent) {
    log.debug('ContestStore.registerFilter()');
    // Push the filter into the state filter stack.
    this.filters = this.filters.concat(filterComponent);
  },


  /**
   * Sort the data by providing a column key.
   *
   * @param  {string} key -  The column key to sort by.
   */
  sortByKey: function(key) {
    // Set the sort states.
    // Flip the sort if it's the currently sorted column.
    var direction = this.data.sortDirection;

    if (this.data.sortKey === key) {
      direction = this.data.sortDirection === 'desc' ? 'asc' : 'desc';
    }

    // Regardless of the sort direction, set the new sortKey.
    this.data.sortKey = key;
    this.data.sortDirection = direction;
    log.debug('Sort column: ' + key + ' - ' + this.data.sortDirection);
    this.filterContests();
  },


  /**
   * A hook for filters to notify us that one of the filters has changed and this
   * store needs to re-filter the data.
   *
   * @param {string} filterName - The name of the filter component.
   */
  filterUpdated: function(filterName, filter) {
    log.debug('DataTable.filterUpdated() - ' + filterName, filter);
    this.data.activeFilters[filterName] = filter;
    // When a filter is updated, update our stored display rows.
    this.filterContests();
  }

});


module.exports = ContestStore;
