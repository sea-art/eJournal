import auth from '@/api/auth'

export default {
    /* Return te needed variables for course/assignment create, connect and select
     */
    get_lti_params_from_jwt (jwtParams) {
        return auth.authenticatedGet('/get_lti_params_from_jwt/' + jwtParams + '/')
            .then(response => response.data)
    }
}
