import auth from '@/api/auth'

export default {

    update (cID, data) {
        return auth.update('roles/' + cID, {roles: data})
            .then(response => response.data.role)
    },

    delete (cID, name) {
        return auth.delete('roles/' + cID, {name: name})
            .then(response => response.data)
    },

    getFromCourse (id) {
        return auth.get('roles', {course_id: id})
            .then(response => response.data.roles)
    }

}
