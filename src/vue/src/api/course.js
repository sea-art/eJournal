import auth from '@/api/auth'

export default {

    /* Get user courses.
     * Requests all the users courses.
     * returns a list of all courses.
     */
    get_user_courses () {
        auth.authenticated_get('/get_user_courses/')
            .then(response => {
                console.log('Success')
                console.log(response)
                return response
            })
            .catch(error => {
                console.error(error)
            })
    }
}
