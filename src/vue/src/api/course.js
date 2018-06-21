import auth from '@/api/auth'

export default {
    /* Get data of a course specified with its ID. */
    get_course_data (cID) {
        return auth.authenticatedGet('/get_course_data/' + cID + '/')
            .then(response => response.data.course)
    },

    /* Get user courses.
     * Requests all the users courses.
     * returns a list of all courses.
     */
    get_user_courses () {
        return auth.authenticatedGet('/get_user_courses/')
            .then(response => response.data.courses)
    },

    get_users (cID) {
        return auth.authenticatedGet('/get_course_users/' + cID + '/')
            .then(response => response.data)
    },

    /* Create a new course. */
    create_new_course (name, abbr, startdate) {
        return auth.authenticatedPost('/create_new_course/', {
            name: name,
            abbr: abbr,
            startdate: startdate
        }).then(response => response.data)
    },

    /* Updates an existing course. */
    update_course (cID, name, abbr, startDate) {
        return auth.authenticatedPost('/update_course/', {
            cID: cID,
            name: name,
            abbr: abbr,
            startDate: startDate
        }).then(response => response.data.course)
    },

    /* Deletes an existing course. */
    delete_course (cID) {
        return auth.authenticatedPost('/delete_course/', {
            cID: cID
        }).then(response => response.data.result)
    },

    /* Updates the role of a student linked to a course. */
    update_user_role_course (uID, cID, role) {
        return auth.authenticatedPost('/update_user_role_course/', {
            uID: uID,
            cID: cID,
            role: role
        }).then(response => response.data.result)
    },

    /* Updates the role of a student linked to a course. */
    delete_user_from_course (uID, cID) {
        return auth.authenticatedPost('/delete_user_from_course/', {
            uID: uID,
            cID: cID
        }).then(response => response.data.result)
    }


}
