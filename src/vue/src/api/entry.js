import auth from '@/api/auth'

export default {
    /* Get entrycomments based on an entryID.
     */
    get_entrycomments (entryID) {
        return auth.authenticatedGet('/get_assignment_journals/' + entryID + '/')
            .then(response => response.data)
            .catch(error => { throw error })
    }
}
