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
 * Redirects the following unsuccessful request responses:
 * UNAUTHORIZED to Login, logs the client out and clears store.
 * FORBIDDEN, NOT_FOUND, INTERNAL_SERVER_ERROR to Error page.
 *
 * The response is thrown and further promise handling should take place.
 * This because this is generic response handling, and we dont know what should happen in case of an error.
 */
function handleError (error, redirect = true, toast = true) {
    const response = error.response
    const status = response.status

    if (toast) {
        this.$toasted.error(error.response.data.description)
    }

    if (redirect && status === statuses.UNAUTHORIZED) {
        store.commit('user/LOGOUT')
        router.push({name: 'Login'})
    } else if (redirect && errorsToRedirect.has(status)) {
        router.push({name: 'ErrorPage',
            params: {
                code: status,
                reasonPhrase: response.statusText,
                description: response.data.description
            }
        })
    }

    throw error
}

function validatedSend (func, url, data = null, redirect = true, toast = true) {
    store.commit('connection/OPEN_API_CALL')
    return func(url, data).then(
        resp => {
            setTimeout(function () {
                store.commit('connection/CLOSE_API_CALL')
            }, 300)
            return resp
        }, error =>
            store.dispatch('user/validateToken', error).then(_ =>
                func(url, data).then(resp => {
                    setTimeout(function () {
                        store.commit('connection/CLOSE_API_CALL')
                    }, 300)
                    return resp
                })
            )
    ).catch(error => {
        setTimeout(function () {
            store.commit('connection/CLOSE_API_CALL')
        }, 300)
        return handleError(error, redirect, toast)
    })
}

function unvalidatedSend (func, url, data = null, redirect = true, toast = true) {
    store.commit('connection/OPEN_API_CALL')
    return func(url, data).then(
        resp => {
            setTimeout(function () {
                store.commit('connection/CLOSE_API_CALL')
            }, 300)
            return resp
        }, error => {
            setTimeout(function () {
                store.commit('connection/CLOSE_API_CALL')
            }, 300)
            return handleError(error, redirect, toast)
        })
}

function improveUrl (url, data = null) {
    if (url[0] !== '/') url = '/' + url
    if (url.slice(-1) !== '/' && !url.includes('?')) url += '/'
    if (data) {
        url += '?'
        for (var key in data) { url += key + '=' + encodeURIComponent(data[key]) + '&' }
        url = url.slice(0, -1)
    }

    return url
}
/*
 * Previous functions are 'private', following are 'public'.
 */
export default {

    /* Create a user and add it to the database. */
    register (username, password, firstname, lastname, email, jwtParams = null) {
        return unvalidatedSend(connection.conn.post, improveUrl('users'), {
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
        return unvalidatedSend(connection.conn.post, improveUrl('forgot_password'), {username: username, email: email})
    },

    /* Recover password */
    recoverPassword (username, recoveryToken, newPassword) {
        return unvalidatedSend(connection.conn.post, improveUrl('recover_password'), {username: username, recovery_token: recoveryToken, new_password: newPassword})
    },

    get (url, data = null, redirect = true, toast = true) {
        return validatedSend(connection.conn.get, improveUrl(url, data), null, redirect, toast)
    },
    post (url, data, redirect = true, toast = true) {
        return validatedSend(connection.conn.post, improveUrl(url), data, redirect, toast)
    },
    patch (url, data, redirect = true, toast = true) {
        return validatedSend(connection.conn.patch, improveUrl(url), data, redirect, toast)
    },
    delete (url, data = null, redirect = true, toast = true) {
        return validatedSend(connection.conn.delete, improveUrl(url, data), null, redirect, toast)
    },
    uploadFile (url, data, redirect = true, toast = true) {
        return validatedSend(connection.connFile.post, improveUrl(url), data, redirect, toast)
    },
    uploadFileEmail (url, data, redirect = true, toast = true) {
        return validatedSend(connection.connFileEmail.post, improveUrl(url), data, redirect, toast)
    },
    downloadFile (url, data, redirect = true, toast = true) {
        return validatedSend(connection.connFile.get, improveUrl(url, data), null, redirect, toast)
    },

    create (url, data, redirect = true, toast = true) { return this.post(url, data, redirect, toast) },
    update (url, data, redirect = true, toast = true) { return this.patch(url, data, redirect, toast) }
}
