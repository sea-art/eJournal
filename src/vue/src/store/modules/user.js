import * as types from '../constants/mutation-types'

const getters = {
    uID: state => state.uID,
    username: state => state.username,
    email: state => state.email,
    profilePicture: state => state.profilePicture,
    firstName: state => state.firstName,
    lastName: state => state.lastName,
    ltiID: state => state.ltiID,
    gradeNotifications: state => state.gradeNotifications,
    commentNotifications: state => state.commentNotifications,
    permissions: state => state.permissions
}

const mutations = {
    // TODO update permissions on login and logout
    [types.LOGIN] (state, data) {
        state.username = data.user.username
        state.email = data.user.email
        state.name = data.user.name
        state.profilePicture = data.user.profilePicture
    },
    [types.LOGOUT] (state) {
        state.uID = null
        state.username = null
        state.email = null
        state.profilePicture = null
        state.firstName = null
        state.lastName = null
        state.ltiID = null
        state.gradeNotifications = null
        state.commentNotifications = null
        state.permissions = null
    }
}

export default {
    namespaced: true,
    state: {
        uID: null,
        username: null,
        email: null,
        profilePicture: null,
        firstName: null,
        lastName: null,
        ltiID: null,
        gradeNotifications: null,
        commentNotifications: null,
        permissions: null
    },
    getters,
    mutations
}
