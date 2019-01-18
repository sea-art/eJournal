import * as types from '../constants/mutation-types.js'
import * as preferenceOptions from '../constants/preference-types.js'

const getters = {
    todoSortBy: state => state.todo.sortBy,
    journalSortAscending: state => state.journal.sortAscending,
    journalGroupFilter: state => state.journal.groupFilter,
    journalSearchValue: state => state.journal.searchValue,
    journalSortBy: state => state.journal.sortBy,
    courseMembersSortAscending: state => state.courseMembers.sortAscending,
    courseMembersViewEnrolled: state => state.courseMembers.viewEnrolled,
    courseMembersGroupFilter: state => state.courseMembers.groupFilter,
    courseMembersSearchValue: state => state.courseMembers.searchValue,
    courseMembersSortBy: state => state.courseMembers.sortBy,
    assignmentOverviewSortAscending: state => state.assignmentOverview.sortAscending,
    assignmentOverviewSearchValue: state => state.assignmentOverview.searchValue,
    assignmentOverviewSortBy: state => state.assignmentOverview.sortBy
}

const mutations = {
    [types.SET_TODO_SORT_BY] (state, sortByOption) {
        if (!preferenceOptions.TODO_SORT_OPTIONS.has(sortByOption)) { throw new Error('Invalid TODO sorting option.') }
        state.todo.sortBy = sortByOption
    },
    [types.SET_JOURNAL_SORT_ASCENDING] (state, sortAscending) {
        state.journal.sortAscending = sortAscending
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
    },
    [types.SET_COURSE_MEMBERS_SORT_ASCENDING] (state, sortAscending) {
        state.courseMembers.sortAscending = sortAscending
    },
    [types.SET_COURSE_MEMBERS_VIEW_ENROLLED] (state, viewEnrolled) {
        state.courseMembers.viewEnrolled = viewEnrolled
    },
    [types.SET_COURSE_MEMBERS_GROUP_FILTER] (state, groupFilter) {
        state.courseMembers.groupFilter = groupFilter
    },
    [types.SET_COURSE_MEMBERS_SEARCH_VALUE] (state, searchValue) {
        state.courseMembers.searchValue = searchValue
    },
    [types.SET_COURSE_MEMBERS_SORT_BY] (state, sortByOption) {
        if (!preferenceOptions.COURSE_MEMBER_SORT_OPTIONS.has(sortByOption)) { throw new Error('Invalid course member sorting option.') }
        state.courseMembers.sortBy = sortByOption
    },
    [types.SET_ASSIGNMENT_OVERVIEW_SORT_ASCENDING] (state, sortAscending) {
        state.assignmentOverview.sortAscending = sortAscending
    },
    [types.SET_ASSIGNMENT_OVERVIEW_SEARCH_VALUE] (state, searchValue) {
        state.assignmentOverview.searchValue = searchValue
    },
    [types.SET_ASSIGNMENT_OVERVIEW_SORT_BY] (state, sortByOption) {
        if (!preferenceOptions.ASSIGNMENT_OVERVIEW_SORT_OPTIONS.has(sortByOption)) { throw new Error('Invalid assignment overview sorting option.') }
        state.assignmentOverview.sortBy = sortByOption
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
            viewEnrolled: true,
            groupFilter: null,
            searchValue: '',
            sortBy: 'name'
        },
        assignmentOverview: {
            sortAscending: true,
            searchValue: '',
            sortBy: 'name'
        }
    },
    getters,
    mutations
}
