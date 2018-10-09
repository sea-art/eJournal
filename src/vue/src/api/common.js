import auth from '@/api/auth'

export default {
    /* Common file for multi-purpose api calls. */
    getNames (data) {
        return auth.get('names/' + (data.cID || 0) + '/' + (data.aID || 0) + '/' + (data.jID || 0), null, true)
            .then(response => response.data.names)
    },

    getPermissions (courseID = null) {
        if (courseID) {
            return auth.get('roles/0', {course_id: courseID})
                .then(response => response.data.role)
        }
        return auth.get('roles/0')
            .then(response => response.data.role)
    }
}
