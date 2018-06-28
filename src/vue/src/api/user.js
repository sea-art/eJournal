import auth from '@/api/auth'

export default {
    /* Get own user data. */
    getOwnUserData () {
        return auth.authenticatedGet('/get_own_user_data/')
            .then(response => response.data.user)
    },
    /* Get user data.
     * Get all the profile data and all the data like entries etc.
     */
    getUserData (uID) {
        return auth.authenticatedGet('/get_user_data/' + uID + '/')
            .then(response => response.data)
    },

    /* Update user data. */
    updateUserData (username, firstName, lastName) {
        return auth.authenticatedPost('/update_user_data/', {username: username, first_name: firstName, last_name: lastName})
    },

    /* Update profile picture. */
    updateProfilePicture (file) {
        return auth.authenticatedFilePost('/update_user_data/', {picture: file})
    },

    /* Change whether the user gets grade notification or not.
     * if getsNotified is "true" the users gets notified by mail when a grade changes.
     * if getsNotified is "false" the users WONT  get notified by mail when a grade changes.
     * else nothing changes (invalid argument).
     */
    updateGradeNotification (getsNotified) {
        return auth.authenticatedPost('/update_grade_notification/', {new_value: getsNotified}).then(r => r.data.new_value)
    },

    /* Change whether the user gets comment notification or not.
     * if getsNotified is "true" the users gets notified by mail when a there is a new comment.
     * if getsNotified is "false" the users WONT  get notified by mail when a there is a new comment.
     * else nothing changes (invalid argument).
     */
    updateCommentNotification (getsNotified) {
        return auth.authenticatedPost('/update_comment_notification/', {new_value: getsNotified}).then(r => r.data.new_value)
    }
}
