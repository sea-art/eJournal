import auth from '@/api/auth.js'

export default {
    update (id, data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.update(`users/${id}`, data, connArgs)
            .then(response => response.data.user)
    },

    download (id, fileName, entryID, nodeID, contentID, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.downloadFile(`users/${id}/download`, {
            file_name: fileName,
            entry_id: entryID,
            node_id: nodeID,
            content_id: contentID,
        }, connArgs)
    },

    GDPR (id, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.downloadFile(`users/${id}/GDPR/`, null, connArgs)
    },

    /* Upload an image that is base64 encoded. */
    updateProfilePictureBase64 (file, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.post('users/set_profile_picture/', { file }, connArgs)
    },

    /* Verify email adress using a given token. */
    verifyEmail (username, token, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.post('/verify_email/', { username, token }, connArgs)
    },

    /* Request an email verification token for the given users email adress. */
    requestEmailVerification (email, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.post('/request_email_verification/', { email }, connArgs)
    },
}
