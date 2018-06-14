import auth from '@/api/auth'

export default {
    /* Get assignment journals.
     * Requests all the assignment journals.
     * returns a list of all journals.
     */
    get_assignment_journals (cID) {
        return auth.authenticatedGet('/get_assignment_journals/' + cID + '/')
            .then(response => response.data.journals)
            .catch(error => { throw error })
    }
}
