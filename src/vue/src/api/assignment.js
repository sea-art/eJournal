import auth from '@/api/auth'

export default {

    get (aID, cID = null) {
        return auth.get('assignments/' + aID, {course_id: cID})
            .then(response => response.data.assignment)
    },

    create (data) {
        return auth.create('assignments', data)
            .then(response => response.data.assignment)
    },

    update (id, data) {
        return auth.update('assignments/' + id, data)
            .then(response => response.data.assignment)
    },

    delete (aID, cID) {
        return auth.delete('assignments/' + aID, {course_id: cID})
            .then(response => response.data)
    },

    getAllFromCourse (cID) {
        if (cID) {
            return auth.get('assignments', {course_id: cID})
                .then(response => response.data.assignments)
        }
        return auth.get('assignments')
            .then(response => response.data.assignments)
    },

    getUpcoming (cID = null) {
        if (cID) {
            return auth.get('assignments/upcomming', {course_id: cID})
                .then(response => response.data.upcomming)
        }
        return auth.get('assignments/upcomming')
            .then(response => response.data.upcomming)
    },

    getWithLti (id) {
        return auth.get('assignments/' + id, {lti: true}, true)
    }
}
