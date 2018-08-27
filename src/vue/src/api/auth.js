import connection from '@/api/connection'
import statuses from '@/utils/constants/status_codes.js'
import router from '@/router'
import store from '@/store'

const errorsToRedirect = new Set([
    statuses.FORBIDDEN,
    statuses.NOT_FOUND,
    statuses.INTERNAL_SERVER_ERROR
])

/*
 * Redirects the following unsuccessfull request responses:
 * UNAUTHORIZED to Login.
 * FORBIDDEN, NOT_FOUND, INTERNAL_SERVER_ERROR to Error page.
 *
 * If nothing is matched or no redirect is True, the response is thrown and further promise handling should take place.
 * This because this is generic response handling, and we dont know what should happen in case of an error.
 */
function handleError (error, noRedirect = false) {
    console.log('Handling error.')
    const response = error.response
    const status = response.status
    const description = 'Placeholder due to varied error format' // TODO handle properly

    if (!noRedirect && status === statuses.UNAUTHORIZED) {
        router.push({name: 'Login'})
    } else if (!noRedirect && errorsToRedirect.has(status)) {
        router.push({name: 'ErrorPage',
            params: {
                code: status,
                reasonPhrase: response.statusText,
                description: description
            }
        })
    } else {
        throw error
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
            })
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
        return this.authenticatedPost('/update_password/', {new_password: newPassword, old_password: oldPassword})
    },

    /* Forgot password.
     * Checks if a user is known by the given email or username. Sends an email with a link to reset the password. */
    forgotPassword (username, email) {
        return connection.conn.post('/forgot_password/', {username: username, email: email})
    },

    /* Recover password */
    recoverPassword (username, recoveryToken, newPassword) {
        return connection.conn.post('/recover_password/', {username: username, recovery_token: recoveryToken, new_password: newPassword})
    },

    /* Run an authenticated post or get request.
    *  The authorization header is set by default setting in main.js, this allows access to protected resources.
     * If the first request is rejected due to an invalid token, the user data (including token) is cleared, and the error
     * is handled in handle error.
     * Returns a Promise to handle the request.
     */
    authenticatedPost (url, data, noRedirect = false) {
        return connection.conn.post(url, data)
            .catch(error => store.dispatch('user/verifyLogin', error)
                .then(_ => connection.conn.post(url, data)))
            .catch(error => handleError(error, noRedirect))
    },
    authenticatedGet (url, noRedirect = false) {
        return connection.conn.get(url)
            .catch(error => store.dispatch('user/verifyLogin', error)
                .then(_ => connection.conn.get(url)))
            .catch(error => handleError(error, noRedirect))
    },

    authenticatedPostFile (url, data, noRedirect = false) {
        return connection.connFile.post(url, data)
            .catch(error => store.dispatch('user/verifyLogin', error)
                .then(_ => connection.connFile.post(url, data)))
            .catch(error => handleError(error, noRedirect))
    },
    authenticatedGetFile (url, data, noRedirect = false) {
        return connection.connFile.get(url, data)
            .catch(error => store.dispatch('user/verifyLogin', error)
                .then(_ => connection.connFile.get(url, data)))
            .catch(error => handleError(error, noRedirect))
    }
}
