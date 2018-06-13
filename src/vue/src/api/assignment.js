import auth from '@/api/auth'

export default {
    /* Get course assignments.
     * Requests all the course assignments.
     * returns a list of all assignments.
     */
    get_course_assignments (cID) {
        return auth.authenticated_get('/get_course_assignments/'+cID+'/')
            .then(response => response.data.assignments)
            .catch(error => { throw error })
    }
}
