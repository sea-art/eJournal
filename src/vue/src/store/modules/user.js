import Vue from 'vue'
import * as types from '../constants/mutation-types.js'
import connection from '@/api/connection.js'
import auth from '@/api/auth.js'

const getters = {
    jwtAccess: state => state.jwtAccess,
    jwtRefresh: state => state.jwtRefresh,
    uID: state => state.uID,
    username: state => state.username,
    email: state => state.email,
    verifiedEmail: state => state.verifiedEmail,
    profilePicture: state => state.profilePicture,
    firstName: state => state.firstName,
    lastName: state => state.lastName,
    ltiID: state => state.ltiID,
    gradeNotifications: state => state.gradeNotifications,
    commentNotifications: state => state.commentNotifications,
    permissions: state => state.permissions
}

const mutations = {
    [types.LOGIN] (state, data) {
        state.jwtAccess = data.access
        state.jwtRefresh = data.refresh
    },
    [types.HYDRATE_USER] (state, data) {
        const userData = data.user_data
        const permissions = data.all_permissions

        state.uID = userData.uID
        state.username = userData.username
        state.email = userData.email
        state.verifiedEmail = userData.verified_email
        state.profilePicture = userData.picture
        state.firstName = userData.first_name
        state.lastName = userData.last_name
        state.ltiID = userData.lti_id
        state.gradeNotifications = userData.grade_notifications
        state.commentNotifications = userData.comment_notifications
        state.permissions = permissions
    },
    [types.LOGOUT] (state) {
        state.jwtAccess = null
        state.jwtRefresh = null
        state.uID = null
        state.username = null
        state.email = null
        state.verifiedEmail = null
        state.profilePicture = null
        state.firstName = null
        state.lastName = null
        state.ltiID = null
        state.gradeNotifications = null
        state.commentNotifications = null
        state.permissions = null
    }
}

const actions = {
    login ({ commit, state }, { username, password }) {
        return connection.conn.post('/token/', {username: username, password: password}).then(response => {
            // TODO move local storage to store checks
            localStorage.setItem('jwt_access', response.data.access)
            localStorage.setItem('jwt_refresh', response.data.refresh)
            commit(types.LOGIN, response.data)

            auth.authenticatedGet('/get_user_store_data/').then(response => {
                console.log(response)
                commit(types.HYDRATE_USER, response.data)
            }, error => {
                Vue.toasted.error(error.response.description)
                // Login success but hydration failed
                throw error
            })
        })
    },
    logout ({commit, state}) {
        return Promise.all([
            // Example how to access different module mutation
            // commit(`module/${types.MUTATION_TYPE}`, null, { root: true })
            commit(types.LOGOUT)
        ])
    }
}

export default {
    namespaced: true,
    state: {
        jwtAccess: null,
        jwtRefresh: null,
        uID: null,
        username: null,
        email: null,
        verifiedEmail: null,
        profilePicture: null,
        firstName: null,
        lastName: null,
        ltiID: null,
        gradeNotifications: null,
        commentNotifications: null,
        permissions: null
    },
    getters,
    mutations,
    actions
}
