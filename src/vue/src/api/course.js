import auth from '@/api/auth'

export default {
    /* Get user courses.
     * Requests all the users courses.
     * returns a list of all courses.
     */
    get_user_courses () {
        return auth.authenticated_get('/get_user_courses/')
            .then(response => {
                return response.data.courses
            })
            .catch(error => {
                throw error
            })
    }
}
