import auth from '@/api/auth'

export default {
    /* Get course assignments.
     * Requests all the course assignments.
     * returns a list of all assignments.
     */
    get_course_assignments (cID) {
        return auth.authenticatedGet('/get_course_assignments/' + cID + '/')
            .then(response => response.data.assignments)
    },
    /* Get upcomming deadlines. */
    get_upcoming_deadlines () {
        return auth.authenticatedGet('/get_upcoming_deadlines/')
            .then(response => response.data.deadlines)
    },
    /* Create a new assignment. */
    create_new_assignment (name, description, cID) {
        return auth.authenticatedPost('/create_new_assignment/', {
            name: name,
            description: description,
            courseID: cID
        }).then(response => response.data)
    }
}
