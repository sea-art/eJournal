import auth from '@/api/auth'

export default {
    /* Get the user's permissions in a course. */
    get_course_permissions (cID) {
        return auth.authenticatedGet('/get_course_permissions/' + cID + '/')
            .then(response => response.data.permissions)
    }
}
