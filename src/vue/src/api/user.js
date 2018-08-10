import auth from '@/api/auth'
import connection from '@/api/connection'

export default {
    /* Create a user and add it to the database. */
    createUser (username, password, firstname, lastname, email, jwtParams = null) {
        return connection.conn.post('/create_lti_user/', {
            username: username,
            password: password,
            first_name: firstname,
            last_name: lastname,
            email: email,
            jwt_params: jwtParams
        }).then(response => response.data.user)
    },

    /* Update user data with lti credentials. */
    updateLtiIdToUser (jwtParams) {
        return auth.authenticatedPost('/update_lti_id_to_user/', {
            jwt_params: jwtParams
        }).then(response => response.data.user)
    },

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
        return auth.authenticatedPost('/update_user_data/', {
            username: username,
            first_name: firstName,
            last_name: lastName
        })
    },

    /* Update user file. */
    updateUserFile (formData) {
        return auth.authenticatedPostFile('/update_user_file/', formData)
    },

    /* Upload an image that is base64 encoded. */
    updateProfilePictureBase64 (urlData) {
        return auth.authenticatedPost('/update_user_profile_picture/', { urlData: urlData })
    },

    /* Change whether the user gets grade notification or not.
     * if getsNotified is "true" the users gets notified by mail when a grade changes.
     * if getsNotified is "false" the users WONT  get notified by mail when a grade changes.
     * else nothing changes (invalid argument).
     */
    updateGradeNotification (getsNotified) {
        return auth.authenticatedPost('/update_grade_notification/', {
            new_value: getsNotified
        }).then(r => r.data.new_value)
    },

    /* Change whether the user gets comment notification or not.
     * if getsNotified is "true" the users gets notified by mail when a there is a new comment.
     * if getsNotified is "false" the users WONT  get notified by mail when a there is a new comment.
     * else nothing changes (invalid argument).
     */
    updateCommentNotification (getsNotified) {
        return auth.authenticatedPost('/update_comment_notification/', {
            new_value: getsNotified
        }).then(r => r.data.new_value)
    }
}
