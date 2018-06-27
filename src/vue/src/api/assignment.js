import auth from '@/api/auth'

export default {
    /* Get data of a cassignment specified with its ID. */
    get_assignment_data (cID, aID) {
        return auth.authenticatedGet('/get_assignment_data/' + cID + '/' + aID + '/')
            .then(response => response.data.assignment)
    },

    /* Get course assignments.
     * Requests all the course assignments.
     * returns a list of all assignments.
     */
    get_course_assignments (cID) {
        return auth.authenticatedGet('/get_course_assignments/' + cID + '/')
            .then(response => response.data.assignments)
    },

    /* Get an assignments by filtering on the lti_id.
     * returns one assignment or none.
     */
    get_assignment_by_lti_id (ltiId) {
        return auth.authenticatedGet('/get_assignment_by_lti_id/' + ltiId + '/')
            .then(response => response.data.assignment)
    },

    /* Get upcomming deadlines. */
    get_upcoming_deadlines () {
        return auth.authenticatedGet('/get_upcoming_deadlines/')
            .then(response => response.data.deadlines)
    },

    /* Create a new assignment. */
    create_new_assignment (name, description, cID, ltiID = null, pointsPossible = null) {
        return auth.authenticatedPost('/create_new_assignment/', {
            name: name,
            description: description,
            cID: cID,
            lti_id: ltiID,
            points_possible: pointsPossible
        }).then(response => response.data)
    },

    /* Updates an existing assignment. */
    update_assignment (aID, name, description) {
        return auth.authenticatedPost('/update_assignment/', {
            aID: aID,
            name: name,
            description: description
        }).then(response => response.data.assignment)
    },

    /* Connect an existing course to lti course. */
    connect_assignment_lti (aID, ltiID, pointsPossible) {
        return auth.authenticatedPost('/connect_assignment_lti/', {
            aID: aID,
            lti_id: ltiID,
            points_possible: pointsPossible
        }).then(response => response.data.assignment)
    },

    /* Deletes an existing assignment. */
    delete_assignment (aID) {
        return auth.authenticatedPost('/delete_assignment/', {
            aID: aID
        }).then(response => response.data.result)
    }

}
