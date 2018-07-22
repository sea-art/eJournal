import auth from '@/api/auth'

export default {
    /* Get entrycomments based on an eID. */
    getEntryComments (eID) {
        return auth.authenticatedGet('/get_entrycomments/' + eID + '/')
            .then(response => response.data)
    },
    /* Create Entry Comment with given text, author and entry. */
    createEntryComment (eID, uID, text) {
        return auth.authenticatedPost('/create_entrycomment/', {
            eID: eID,
            uID: uID,
            text: text
        })
            .then(response => response.data)
    },
    deleteEntryComment (ecID) {
        return auth.authenticatedPost('/delete_entrycomment/', {
            ecID: ecID
        })
            .then(response => response.data)
    },
    /* Update Entry Comment with given text and EntryComment. */
    updateEntryComments (ecID, text) {
        return auth.authenticatedGet('/update_entrycomments/', {
            ecID: ecID,
            text: text
        })
            .then(response => response.data)
    }
}
