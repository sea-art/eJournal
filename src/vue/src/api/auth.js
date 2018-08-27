import connection from '@/api/connection'
import statuses from '@/utils/status_codes.js'
import router from '@/router'

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

/*
 * Redirects the following unsuccessfull request responses:
 * UNAUTHORIZED to Login.
 * FORBIDDEN, NOT_FOUND, INTERNAL_SERVER_ERROR to Error page.
 *
 * If nothing is matched or no redirect is True, the response is thrown and further promise handling should take place.
 * This because this is generic response handling, and we dont know what should happen in case of an error.
 */
function handleError (error, noRedirect = false) {
    const response = error.response
    const status = response.status

    if (!noRedirect && status === statuses.UNAUTHORIZED) {
        router.push({name: 'Login'})
    } else if (!noRedirect && (status === statuses.FORBIDDEN || status === statuses.NOT_FOUND || status === statuses.INTERNAL_SERVER_ERROR)) {
        router.push({name: 'ErrorPage',
            params: {
                code: status,
                reasonPhrase: response.statusText,
                description: response.data.description ? response.data.description : ''
            }
        })
    } else {
        throw error
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

    /* Create a user and add it to the database. */
    register (username, password, firstname, lastname, email, jwtParams = null) {
        return connection.conn.post('/create_lti_user/', {
            username: username,
            password: password,
            first_name: firstname,
            last_name: lastname,
            email: email,
            jwt_params: jwtParams
        })
            .then(response => { return response.data.user })
    },

    /* Change password. */
    changePassword (newPassword, oldPassword) {
        return this.update('users/password', { new_password: newPassword, old_password: oldPassword })
    },

    /* Forgot password.
     * Checks if a user is known by the given email or username. Sends an email with a link to reset the password. */
    forgotPassword (username, email) {
        return this.post('forgot_password', {username: username, email: email})
    },

    /* Recover password */
    recoverPassword (username, recoveryToken, newPassword) {
        return this.post('recover_password', {username: username, recovery_token: recoveryToken, new_password: newPassword})
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

    get (url, data = null, noRedirect = false) {
        if (url[0] !== '/') url = '/' + url
        if (url.slice(-1) !== '/') url += '/'
        if (data) {
            url += '?'
            for (var key in data) { url += key + '=' + data[key] + '&' }
            url = url.slice(0, -1)
        }
        return connection.conn.get(url, getAuthorizationHeader())
            .catch(error => refresh(error)
                .then(_ => connection.conn.post(url, getAuthorizationHeader())))
            .catch(error => handleError(error, noRedirect))
    },
    post (url, data, noRedirect = false) {
        if (url[0] !== '/') url = '/' + url
        if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
        return connection.conn.post(url, data, getAuthorizationHeader())
            .catch(error => refresh(error)
                .then(_ => connection.conn.post(url, data, getAuthorizationHeader())))
            .catch(error => handleError(error, noRedirect))
    },
    create (url, data, noRedirect = false) {
        return this.post(url, data, noRedirect)
    },
    patch (url, data, noRedirect = false) {
        if (url[0] !== '/') url = '/' + url
        if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
        return connection.conn.patch(url, data, getAuthorizationHeader())
            .catch(error => refresh(error)
                .then(_ => connection.conn.patch(url, data, getAuthorizationHeader())))
            .catch(error => handleError(error, noRedirect))
    },
    update (url, data, noRedirect = false) {
        return this.patch(url, data, noRedirect)
    },
    delete (url, data = null, noRedirect = false) {
        if (url[0] !== '/') url = '/' + url
        if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
        if (data) {
            url += '?'
            for (var key in data) { url += key + '=' + data[key] + '&' }
            url = url.slice(0, -1)
        }
        return connection.conn.delete(url, getAuthorizationHeader())
            .catch(error => refresh(error)
                .then(_ => connection.conn.delete(url, getAuthorizationHeader())))
            .catch(error => handleError(error, noRedirect))
    },
    uploadFile (url, data, noRedirect = false) {
        return connection.connFile.post(url, data, getAuthorizationHeader())
            .catch(error => refresh(error)
                .then(_ => connection.connFile.post(url, data, getAuthorizationHeader())))
            .catch(error => handleError(error, noRedirect))
    }
}
