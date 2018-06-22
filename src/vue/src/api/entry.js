import auth from '@/api/auth'

export default {
    /* Get entrycomments based on an entryID. */
    getEntryComments (entryID) {
        return auth.authenticatedGet('/get_entrycomments/' + entryID + '/')
            .then(response => response.data)
    },
    /* Create Entry Comment with given text, author and entry. */
    createEntryComment (entryID, authorID, text) {
        return auth.authenticatedPost('/create_entrycomment/', {
            entryID: entryID,
            authorID: authorID,
            text: text
        })
            .then(response => response.data)
    },
    /* Update Entry Comment with given text and EntryComment. */
    updateEntryComments (entrycommentID, text) {
        return auth.authenticatedGet('/update_entrycomments/', {
            entrycommentID: entrycommentID,
            text: text
        })
            .then(response => response.data)
    }
}
