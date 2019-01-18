import * as types from '../constants/mutation-types.js'
import * as preferenceOptions from '../constants/preference-types.js'

const getters = {
    todoSortBy: state => state.todo.sortBy,
    journalSortAscending: state => state.journal.sortAscending,
    journalGroupFilter: state => state.journal.groupFilter,
    journalSearchValue: state => state.journal.searchValue,
    journalSortBy: state => state.journal.sortBy
}

const mutations = {
    [types.SET_TODO_SORT_BY] (state, sortByOption) {
        if (!preferenceOptions.TODO_SORT_OPTIONS.has(sortByOption)) { throw new Error('Invalid TODO sorting option.') }
        state.todo.sortBy = sortByOption
    },
    [types.SET_JOURNAL_SORT_ASCENDING] (state, ascending) {
        state.journal.sortAscending = ascending
    },
    [types.SET_JOURNAL_GROUP_FILTER] (state, groupFilter) {
        state.journal.groupFilter = groupFilter
    },
    [types.SET_JOURNAL_SEARCH_VALUE] (state, searchValue) {
        state.journal.searchValue = searchValue
    },
    [types.SET_JOURNAL_SORT_BY] (state, sortByOption) {
        if (!preferenceOptions.JOURNAL_SORT_OPTIONS.has(sortByOption)) { throw new Error('Invalid journal sorting option.') }
        state.journal.sortBy = sortByOption
    }
}

export default {
    namespaced: true,
    state: {
        todo: {
            sortBy: 'date'
        },
        journal: {
            sortAscending: true,
            groupFilter: null,
            searchValue: '',
            sortBy: 'markingNeeded'
        },
        courseMembers: {
            sortAscending: true,
            enrolled: true,
            groupFilter: null,
            searchValue: null,
            sortBy: 'name'
        },
        assignmentOverview: {
            sortAscending: true,
            searchValue: null,
            sortBy: 'name'
        }
    },
    getters,
    mutations
}
