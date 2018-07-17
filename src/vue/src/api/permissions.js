import auth from '@/api/auth'

export default {
    /* Get the user's permissions in a course. */
    get_course_permissions (cID) {
        return auth.get('/get_course_permissions/' + cID + '/')
            .then(response => response.data.permissions)
    },

    get_course_roles (cID) {
        return auth.authenticatedGet('/get_course_roles/' + cID + '/')
            .then(response => response.data.roles)
    },

    update_course_roles (cID, roles) {
        return auth.authenticatedPost('/update_course_roles/', {
            cID: cID,
            roles: roles
        })
            .then(response => response.data)
    },

    delete_course_role (cID, name) {
        return auth.authenticatedPost('/delete_course_role/', {
            cID: cID,
            name: name
        })
            .then(response => response.data)
    }
}
