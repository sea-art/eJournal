import auth from '@/api/auth'

export default {
    get (id) {
        return auth.get('participations/' + id)
            .then(response => response.data.participant)
    },

    getEnrolled (id) {
        return auth.get('participations', {course_id: id})
            .then(response => response.data.participants)
    },

    create (data) {
        return auth.create('participations', data)
            .then(response => response.data.participant)
    },

    update (id, data) {
        return auth.update('participations/' + id, data)
            .then(response => response.data.participant)
    },

    delete (cID, uID) {
        return auth.delete('participations/' + cID, {user_id: uID})
            .then(response => response.data)
    },

    getUnenrolled (id, unenrolledQuery) {
        return auth.get('participations/unenrolled', {course_id: id, unenrolled_query: unenrolledQuery})
            .then(response => response.data.participants)
    }

}
