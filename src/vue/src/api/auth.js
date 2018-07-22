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
        if (localStorage.getItem('jwt_refresh') == null) {
            router.app.validToken = false
            throw error
        }

        return connection.conn.post('token/refresh/', {refresh: localStorage.getItem('jwt_refresh')})
            .then(response => {
                localStorage.setItem('jwt_access', response.data.access)
                router.app.validToken = true
            })
            .catch(error => {
                router.app.validToken = false
                throw error
            })
    } else {
        throw error
    }
}
// TODO: Change back to false
function handleResponse (response, noRedirect = true) {
    response = response.response
    if (response.status === 401) { // Unauthorized
        if (!noRedirect) {
            router.push({name: 'Login'})
        }
    } else if (response.status === 403 || // Forbidden
          response.status === 404) { // Not found)
        if (!noRedirect) {
            Vue.toasted.error(response.data.result + ': ' + response.data.description)
            router.push({name: 'ErrorPage',
                params: {
                    code: response.status,
                    message: response.data.result,
                    description: response.data.description
                }
            })
        }
    } else if (response.status === 500) { // Internal server error
        if (!noRedirect) {
            Vue.toasted.error(response.data.result + ': ' + response.data.description)
            router.push({name: 'ErrorPage',
                params: {
                    code: response.status,
                    message: 'Internal Server Error',
                    description: response.data.description
                }
            })
        }
    } else if (response.status === 400) { // Bad request
        if (response.data.description) {
            Vue.toasted.error(response.data.result + ': ' + response.data.description)
        } else {
            Vue.toasted.error(response.data.result)
        }
    }
    throw response
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
        return this.patch('/users/password', { new_password: newPassword, old_password: oldPassword })
    },

    /* Check if the stored token is valid. */
    testValidToken () {
        if (localStorage.getItem('jwt_access') == null && localStorage.getItem('jwt_refresh') == null) {
            router.app.validToken = false
            return Promise.reject(new Error('Token undefined'))
        }

        return connection.conn.post('/token/verify/', {token: localStorage.getItem('jwt_access')})
            .then(_ => { router.app.validToken = true })
            .catch(error => refresh(error))
    },

    // TODO: remove this old function
    authenticatedGet () {
        return this.get('courses')
    },

    get (url, noRedirect = false) {
        if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
        return connection.conn.get(url, getAuthorizationHeader())
            .then(response => response.data.result)
            .catch(error => refresh(error)
                .then(_ => connection.conn.post(url, getAuthorizationHeader())))
            .catch(error => handleResponse(error, noRedirect))
    },
    create (url, data, noRedirect = false) {
        if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
        return connection.conn.post(url, data, getAuthorizationHeader())
            .then(response => response.data)
            .catch(error => refresh(error)
                .then(_ => connection.conn.post(url, data, getAuthorizationHeader())))
            .catch(error => handleResponse(error, noRedirect))
    },
    update (url, data, noRedirect = false) {
        if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
        return connection.conn.patch(url, data, getAuthorizationHeader())
            .then(response => response.data)
            .catch(error => refresh(error)
                .then(_ => connection.conn.patch(url, data, getAuthorizationHeader())))
            .catch(error => handleResponse(error, noRedirect))
    },
    delete (url, noRedirect = false) {
        if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
        return connection.conn.delete(url, getAuthorizationHeader())
            .then(response => response.data)
            .catch(error => refresh(error)
                .then(_ => connection.conn.delete(url, getAuthorizationHeader())))
            .catch(error => handleResponse(error, noRedirect))
    },
    uploadFile (url, data, noRedirect = false) {
        return connection.connFile.post(url, data, getAuthorizationHeader())
            .catch(error => refresh(error)
                .then(_ => connection.connFile.post(url, data, getAuthorizationHeader())))
            .catch(error => handleResponse(error, noRedirect))
    }
}
