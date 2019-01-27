import Vue from 'vue'
import * as types from '../constants/mutation-types.js'
import * as preferenceOptions from '../constants/preference-types.js'
import connection from '@/api/connection.js'
import sanitization from '@/utils/sanitization.js'

const getters = {
    // Stored user preferences.
    gradeNotifications: state => state.gradeNotifications,
    commentNotifications: state => state.commentNotifications,

    // Search filters.
    todoSortBy: state => state.todo.sortBy,
    journalSortAscending: state => state.journal.sortAscending,
    journalGroupFilter: state => state.journal.groupFilter,
    journalSelfSetGroupFilter: state => state.journal.selfSetGroupFilter,
    journalSearchValue: state => state.journal.searchValue,
    journalSortBy: state => state.journal.sortBy,
    journalAID: state => state.journal.aID,
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
    [types.HYDRATE_PREFERENCES] (state, data) {
        const preferences = data.preferences

        state.gradeNotifications = preferences.grade_notifications
        state.commentNotifications = preferences.comment_notifications
    },
    [types.SET_GRADE_NOTIFICATION] (state, val) {
        state.gradeNotifications = val
    },
    [types.SET_COMMENT_NOTIFICATION] (state, val) {
        state.commentNotifications = val
    },
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
    [types.SET_JOURNAL_SELF_SET_GROUP_FILTER] (state, selfSet) {
        state.journal.selfSetGroupFilter = selfSet
    },
    [types.SET_JOURNAL_SEARCH_VALUE] (state, searchValue) {
        state.journal.searchValue = searchValue
    },
    [types.SET_JOURNAL_SORT_BY] (state, sortByOption) {
        if (!preferenceOptions.JOURNAL_SORT_OPTIONS.has(sortByOption)) { throw new Error('Invalid journal sorting option.') }
        state.journal.sortBy = sortByOption
    },
    [types.SWITCH_JOURNAL_ASSIGNMENT] (state, aID) {
        if (aID !== state.journal.aID) {
            state.journal.aID = aID
            state.journal.sortAscending = true
            state.journal.groupFilter = null
            state.journal.selfSetGroupFilter = false
            state.journal.searchValue = ''
            state.journal.sortBy = 'markingNeeded'
        }
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
    },
    [types.RESET_PREFERENCES] (state) {
        state.todo.sortBy = 'date'
        state.journal.aID = null
        state.journal.sortAscending = true
        state.journal.groupFilter = null
        state.journal.selfSetGroupFilter = false
        state.journal.searchValue = ''
        state.journal.sortBy = 'markingNeeded'
        state.courseMembers.sortAscending = true
        state.courseMembers.viewEnrolled = true
        state.courseMembers.groupFilter = null
        state.courseMembers.searchValue = ''
        state.courseMembers.sortBy = 'name'
        state.assignmentOverview.sortAscending = true
        state.assignmentOverview.searchValue = ''
        state.assignmentOverview.sortBy = 'name'
    }
}

const actions = {
    populateStore ({ commit }) {
        return new Promise((resolve, reject) => {
            connection.conn.get('/preferences/0/').then(response => {
                commit(types.HYDRATE_PREFERENCES, response.data)
                resolve('Store is populated successfully')
            }, error => {
                Vue.toasted.error(sanitization.escapeHtml(error.response.data.description))
                reject(error)
            })
        })
    }
}

export default {
    namespaced: true,
    state: {
        gradeNotifications: null,
        commentNotifications: null,
        todo: {
            sortBy: 'date'
        },
        journal: {
            aID: null,
            sortAscending: true,
            groupFilter: null,
            selfSetGroupFilter: false,
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
    mutations,
    actions
}
