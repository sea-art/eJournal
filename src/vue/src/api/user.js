import auth from '@/api/auth'

export default {
    /* Get own user data. */
    getOwnUserData () {
        return auth.authenticatedGet('/get_own_user_data/')
            .then(response => response.data.user)
    },

    /* Update user data. */
    updateUserData (username, picture) {
        return auth.authenticatedPost('/update_user_data/', {username: username, picture: picture})
    },

    /* Change whether the user gets grade notification or not.
     * if getsNotified is "true" the users gets notified by mail when a grade changes.
     * if getsNotified is "false" the users WONT  get notified by mail when a grade changes.
     * else nothing changes (invalid argument).
     */
    updateGradeNotification (getsNotified) {
        return auth.authenticatedGet('/update_grade_notification/' + getsNotified + '/')
            .then(r => r.new_value)
    },

    /* Change whether the user gets comment notification or not.
     * if getsNotified is "true" the users gets notified by mail when a there is a new comment.
     * if getsNotified is "false" the users WONT  get notified by mail when a there is a new comment.
     * else nothing changes (invalid argument).
     */
    updateCommentNotification (getsNotified) {
        return auth.authenticatedGet('/update_comment_notification/' + getsNotified + '/')
            .then(r => r.new_value)
    }
}
