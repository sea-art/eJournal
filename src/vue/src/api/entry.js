import auth from '@/api/auth'

export default {
    /* Get entrycomments based on an entryID.
     * Create Entry Comment with given text, author and entry.
     * Update Entry Comment with given text and EntryComment.
     */
    get_entrycomments (entryID) {
        return auth.authenticatedGet('/get_assignment_journals/' + entryID + '/')
            .then(response => response.data)
    },
    create_entrycomments (entryID, authorID, text) {
        return auth.authenticatedGet('/create_entrycomments/', {
            entryID: entryID,
            authorID: authorID,
            text: text
        })
            .then(response => response.data)
    },
    update_entrycomments (entrycommentID, text) {
        return auth.authenticatedGet('/update_entrycomments/', {
            entrycommentID: entrycommentID,
            text: text
        })
            .then(response => response.data)
    }
}
