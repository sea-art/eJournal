import auth from '@/api/auth'

export default {

    get (id) {
        return auth.get('courses/' + id)
            .then(response => response.data.course)
    },

    create (data) {
        return auth.create('courses', data)
            .then(response => response.data.course)
    },

    update (id, data) {
        return auth.update('courses/' + id, data)
            .then(response => response.data.course)
    },

    delete (id) {
        return auth.delete('courses/' + id)
            .then(response => response.data)
    },

    getUserEnrolled () {
        return auth.get('courses')
            .then(response => response.data.courses)
    },

    getAsTeacher () {
        return auth.get('courses/is_teacher')
            .then(response => response.data.courses)
    }
}
