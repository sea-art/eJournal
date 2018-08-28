import auth from '@/api/auth'

export default {

    get (id = 0) {
        return auth.get('users/' + id)
            .then(response => response.data.user)
    },

    create (data) {
        return auth.create('users', data)
            .then(response => response.data.user)
    },

    update (id = 0, data = null) {
        return auth.update('users/' + id, data)
            .then(response => response.data.user)
    },

    delete (id = 0) {
        return auth.delete('users/' + id)
            .then(response => response.data)
    },

    download (id = 0, fileName) {
        return auth.get('users/'+ id + '/download', {file: fileName})
    },

    GDPR (id = 0) {
        return auth.get('users/' + id + '/GDPR')
    },

    /* Update user file. */
    updateUserFile (formData) {
        return auth.postFile('/upload/', formData)
    },

    /* Upload an image that is base64 encoded. */
    updateProfilePictureBase64 (file) {
        return auth.post('users/set_profile_picture/', { file: file })
    },

    /* Verify email adress using a given token. */
    verifyEmail (token) {
        return auth.post('/verify_email/', {
            token: token
        })
    },

    /* Request an email verification token for the given users email adress. */
    requestEmailVerification () {
        return auth.post('/request_email_verification/')
    }

    // /* Get user file. */
    // getUserFile (fileName, authorUID) {
    //     return auth.authenticatedGet('/get_user_file/' + fileName + '/' + authorUID + '/')
    // },
}
