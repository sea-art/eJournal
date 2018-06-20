import connection from '@/api/connection'

/* Utility function to get the Authorization header with
 * the JWT token.
 */
function getAuthorizationHeader () {
    return {headers: { Authorization: 'Bearer ' + localStorage.getItem('jwt_access') }}
}

/* Refresh the access token.
 * Requests the api server for a new JWT token, given the refresh token.
 * Stores this new token in jwt_access.
 * Returns a new Promise that can be used to chain more requests.
 */
function refresh () {
    return connection.conn.post('token/refresh/', {refresh: localStorage.getItem('jwt_refresh')})
        .then(response => {
            localStorage.setItem('jwt_access', response.data.access)
        })
}

/*
 * Previous functions are 'private', following are 'public'.
 */
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
    },

    /* Log out.
     * Removes the JWT tokens so that the user can no longer
     * access protected resources.
     */
    logout () {
        localStorage.removeItem('jwt_access')
        localStorage.removeItem('jwt_refresh')
    },

    /* Change password. */
    changePassword (newPassword, oldPassword) {
        return this.authenticatedPost('/update_password/', {new_password: newPassword, old_password: oldPassword})
    },

    /* Run an authenticated post request.
     * This sets the JWT token to the Authorization headers of the request, so that it can access
     * protected resources. If the access JWT token is outdated, it refreshes and tries again.
     * Returns a Promise to handle the request.
     */
    authenticatedPost (url, data) {
        return connection.conn.post(url, data, getAuthorizationHeader())
            .catch(error => {
                if (error.response.data.code === 'token_not_valid') {
                    return refresh().then(_ => connection.conn.post(url, data, getAuthorizationHeader()))
                } else {
                    throw error
                }
            })
    },

    /* Run an authenticated get request.
     * This sets the JWT token to the Authorization headers of the request, so that it can access
     * protected resources. If the access JWT token is outdated, it refreshes and tries again.
     * Returns a Promise to handle the request.
     */
    authenticatedGet (url) {
        return connection.conn.get(url, getAuthorizationHeader())
            .catch(error => {
                if (error.response.data.code === 'token_not_valid') {
                    return refresh().then(_ => connection.conn.get(url, getAuthorizationHeader()))
                } else {
                    throw error
                }
            })
    }
}
