import auth from '@/api/auth'

export default {
    /* Get own user data. */
    get_own_user_data () {
        return auth.authenticatedGet('/get_own_user_data/')
            .then(response => response.data.user)
    },

    /* Change whether the user gets grade notification or not.
     * if getsNotified is "true" the users gets notified by mail when a grade changes.
     * if getsNotified is "false" the users WONT  get notified by mail when a grade changes.
     * else nothing changes (invalid argument).
     */
    update_grade_notification (getsNotified) {
        return auth.authenticatedGet('/update_grade_notification/' + getsNotified + '/').then(r => r.new_value)
    },

    /* Change whether the user gets comment notification or not.
     * if getsNotified is "true" the users gets notified by mail when a there is a new comment.
     * if getsNotified is "false" the users WONT  get notified by mail when a there is a new comment.
     * else nothing changes (invalid argument).
     */
    update_comment_notification (getsNotified) {
        return auth.authenticatedGet('/update_comment_notification/' + getsNotified + '/').then(r => r.new_value)
    }
}
