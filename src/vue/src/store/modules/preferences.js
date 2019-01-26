import Vue from 'vue'
import * as types from '../constants/mutation-types.js'
import connection from '@/api/connection.js'
import genericUtils from '@/utils/generic_utils.js'
import sanitization from '@/utils/sanitization.js'

const getters = {
    gradeNotifications: state => state.gradeNotifications,
    commentNotifications: state => state.commentNotifications,
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
    },
    getters,
    mutations,
    actions
}
