import connection from '@/api/connection'
import router from '@/router'
import Vue from 'vue'

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
function refresh (error) {
    if (error.response.data.code === 'token_not_valid') {
        return connection.conn.post('token/refresh/', {refresh: localStorage.getItem('jwt_refresh')})
            .then(response => {
                localStorage.setItem('jwt_access', response.data.access)
                router.app.validToken = true
            })
            .catch(_ => {
                if (error.response.data.code === 'token_not_valid') {
                    router.app.validToken = false
                }
                throw error
            })
    } else {
        throw error
    }
}

function handleResponse (response, noRedirect = false) {
    response = response.response
    if (response.status === 401) { // Unauthorized
        console.log(router)
        if (!noRedirect) {
            router.push({name: 'Login'})
        }
    } if (response.status === 403 || // Forbidden
          response.status === 404 || // Not found
          response.status === 500) { // Internal server error
        if (!noRedirect) {
            router.push({name: 'ErrorPage',
                params: {
                    code: response.status,
                    message: response.data.result,
                    description: response.data.description
                }})
        }
    } else if (response.status === 400) { // Bad request
        if (response.data.description) {
            Vue.toasted.error(response.data.result + ': ' + response.data.description)
        } else {
            Vue.toasted.error(response.data.result)
        }
    } else {
        throw response
    }
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
                router.app.validToken = true
            })
    },

    /* Log out.
     * Removes the JWT tokens so that the user can no longer
     * access protected resources.
     */
    logout () {
        localStorage.removeItem('jwt_access')
        localStorage.removeItem('jwt_refresh')
        router.app.validToken = false
    },

    /* Change password. */
    changePassword (newPassword, oldPassword) {
        return this.authenticatedPost('/update_password/', {new_password: newPassword, old_password: oldPassword})
    },

    /* Check if the stored token is valid. */
    testValidToken () {
        return this.authenticatedGet('/check_valid_token/', true)
            .then(_ => { router.app.validToken = true })
            .catch(_ => { router.app.validToken = false })
    },

    /* Run an authenticated post request.
     * This sets the JWT token to the Authorization headers of the request, so that it can access
     * protected resources. If the access JWT token is outdated, it refreshes and tries again.
     * Returns a Promise to handle the request.
     */
    authenticatedPost (url, data, noRedirect = false) {
        return connection.conn.post(url, data, getAuthorizationHeader())
            .catch(error => refresh(error))
            .then(connection.conn.post(url, data, getAuthorizationHeader()))
            .catch(error => handleResponse(error, noRedirect))
    },

    /* Run an authenticated get request.
     * This sets the JWT token to the Authorization headers of the request, so that it can access
     * protected resources. If the access JWT token is outdated, it refreshes and tries again.
     * Returns a Promise to handle the request.
     */
    authenticatedGet (url, noRedirect = false) {
        return connection.conn.get(url, getAuthorizationHeader())
            .catch(error => refresh(error, url))
            .then(connection.conn.get(url, getAuthorizationHeader()))
            .catch(error => handleResponse(error, noRedirect))
    }

}
