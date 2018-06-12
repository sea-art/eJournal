import connection from '@/api/connection'

export default {

    /* Log in.
     * Requests the api server for a JWT token.
     * Stores this token in jwt_access and jwt_refresh.
     * Returns a new Promise that can be used to chain more requests.
     */
    login (username, password) {
        return connection.conn.post('/token/', {username: username, password: password})
                .then(response => {
                    localStorage.setItem('jwt_access', response.data.access)
                    localStorage.setItem('jwt_refresh', response.data.refresh)
                })
                .catch(error => {
                    throw error
                })
    },

    /* Log out.
     * Removes the JWT tokens so that the user can no longer
     * access protected resources.
     */
    logout () {
        localStorage.removeItem('jwt_access')
        localStorage.removeItem('jwt_refresh')
    },

    /* Run an authenticated request.
     * This appends the JWT token to the headers of the request, so that it can access
     * protected resources.
     * Returns a Promise to handle the request.
     */
    authenticated_post (url, data, options = {}) {
        connection.conn.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('jwt_access')
        return connection.conn.post(url, data, options)
    },

    authenticated_get (url, options = {}) {
        connection.conn.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('jwt_access')
        console.log(connection.conn.defaults.headers)
        return connection.conn.get(url, options)
    }
}
