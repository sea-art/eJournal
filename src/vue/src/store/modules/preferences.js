import * as types from '../constants/mutation-types.js'

const getters = {
    todoSortByDate: state => state.todo.sortBy.date,
    todoSortByMarkingNeeded: state => state.todo.sortBy.markingNeeded,
    journalSortAscending: state => state.journal.sortAscending,
    journalGroupFilter: state => state.journal.groupFilter,
    journalSearchValue: state => state.journal.searchValue,
    journalSortByMarkingNeeded: state => state.journal.sortBy.markingNeeded,
    journalSortByName: state => state.journal.sortBy.name,
    journalSortByUsername: state => state.journal.sortBy.username
}

const mutations = {
    [types.SET_TODO_SORT_BY_DATE] (state, sortByDate) {
        state.todo.sortBy.date = sortByDate
    },
    [types.SET_TODO_SORT_BY_MARKING_NEEDED] (state, sortByMarkingNeeded) {
        state.todo.sortBy.markingNeeded = sortByMarkingNeeded
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
    [types.SET_JOURNAL_SORT_BY_MARKING_NEEDED] (state, sortByMarkingNeeded) {
        state.journal.sortBy.markingNeeded = sortByMarkingNeeded
    },
    [types.SET_JOURNAL_SORT_BY_NAME] (state, sortByName) {
        state.journal.sortBy.name = sortByName
    },
    [types.SET_JOURNAL_SORT_BY_USERNAME] (state, sortByUsername) {
        state.journal.sortBy.username = sortByUsername
    }
}

export default {
    namespaced: true,
    state: {
        todo: {
            sortBy: {
                date: true,
                markingNeeded: false
            }
        },
        journal: {
            sortAscending: true,
            groupFilter: null,
            searchValue: null,
            sortBy: {
                markingNeeded: true,
                name: false,
                username: false
            }
        }
    },
    getters,
    mutations
}
