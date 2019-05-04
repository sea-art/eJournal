import connection from '@/api/connection.js'
import statuses from '@/utils/constants/status_codes.js'
import router from '@/router'
import store from '@/store'
import sanitization from '@/utils/sanitization.js'
import genericUtils from '@/utils/generic_utils.js'

const ERRORS_TO_REDIRECT = new Set([
    statuses.FORBIDDEN,
    statuses.NOT_FOUND,
    statuses.INTERNAL_SERVER_ERROR,
])

/*
 * Defines how success and error responses are handled and toasted by default.
 *
 * Changes can be made by overwriting the DEFAULT_CONN_ARGS keys in an API call.
 * Handled errors are redirected by default when present in ERRORS_TO_REDIRECT unless redirect set to false.
 * Handled errors messages default to: response.data.description, unless customErrorToast set.
 * Handled successes do not redirect or display a message unless:
 *    - responseSuccessToast set, toasting the response description
 *    - customSuccessToast is set, toasting the given message.
 */
const DEFAULT_CONN_ARGS = {
    redirect: true,
    customSuccessToast: false,
    responseSuccessToast: false,
    customErrorToast: false,
}

/* Sets default connection arguments to missing keys, otherwise use the given connArgs value. */
function packConnArgs (connArgs) {
    if (!(connArgs instanceof Object) || Object.keys(connArgs).length === 0) {
        throw Error('Connection arguments should be a non emtpy object.')
    }

    Object.keys(connArgs).forEach((key) => {
        if (!(key in DEFAULT_CONN_ARGS)) { throw Error(`Unkown connection argument key: ${key}`) }
    })

    return { ...DEFAULT_CONN_ARGS, ...connArgs }
}

/* Toasts an error safely, escaping html and parsing an array buffer. */
function toastError (error, connArgs) {
    if (connArgs.customErrorToast) {
        router.app.$toasted.error(sanitization.escapeHtml(connArgs.customErrorToast))
    } else if (connArgs.customErrorToast !== '') {
        let data
        if (error.response.data instanceof ArrayBuffer) {
            data = genericUtils.parseArrayBuffer(error.response.data)
        } else {
            data = error.response.data
        }

        /* The Django throttle module uses detail as description. */
        const message = data.description ? data.description : data.detail
        if (message) { router.app.$toasted.error(sanitization.escapeHtml(message)) }
    }
}

/* Lowers the connection count and toast a success message
 * if a custom one is provided or responseSuccessToast is set. */
function handleSuccess (resp, connArgs) {
    if (connArgs.responseSuccessToast) {
        let message
        if (resp.data instanceof ArrayBuffer) {
            message = genericUtils.parseArrayBuffer(resp.data).description
        } else {
            message = resp.data.description
        }

        if (message) { router.app.$toasted.success(sanitization.escapeHtml(message)) }
    } else if (connArgs.customSuccessToast) {
        router.app.$toasted.success(sanitization.escapeHtml(connArgs.customSuccessToast))
    }
}

/*
 * Redirects the following unsuccessful request responses:
 * UNAUTHORIZED to Login, logs the client out and clears store.
 * FORBIDDEN, NOT_FOUND, INTERNAL_SERVER_ERROR to Error page.
 *
 * The response is thrown and further promise handling should take place.
 * This because this is generic response handling, and we dont know what should happen in case of an error.
 */
function handleError (error, connArgs) {
    const response = error.response
    const status = response.status

    if (connArgs.redirect && status === statuses.UNAUTHORIZED) {
        store.commit('user/LOGOUT')
        router.push({ name: 'Login' })
        toastError(error, connArgs)
    } else if (connArgs.redirect && ERRORS_TO_REDIRECT.has(status)) {
        router.push({
            name: 'ErrorPage',
            params: {
                code: status,
                reasonPhrase: response.statusText,
                description: response.data.description,
            },
        })
    } else {
        toastError(error, connArgs)
    }

    throw error
}

function initRequest (func, url, data = null, connArgs = DEFAULT_CONN_ARGS) {
    const packedConnArgs = packConnArgs(connArgs)

    return func(url, data).then(
        (resp) => {
            handleSuccess(resp, packedConnArgs)
            return resp
        }, error => handleError(error, packedConnArgs))
}

function improveUrl (url, data = null) {
    let improvedUrl = url
    if (improvedUrl[0] !== '/') { improvedUrl = `/${improvedUrl}` }
    if (improvedUrl.slice(-1) !== '/' && !improvedUrl.includes('?')) { improvedUrl += '/' }
    if (data) {
        improvedUrl += '?'
        Object.keys(data).forEach((key) => { improvedUrl += `${key}=${encodeURIComponent(data[key])}&` })
        improvedUrl = improvedUrl.slice(0, -1)
    }

    return improvedUrl
}
/*
 * Previous functions are 'private', following are 'public'.
 */
export default {
    DEFAULT_CONN_ARGS,

    /* Create a user and add it to the database. */
    register (username, password, fullName, email, jwtParams = null, connArgs = DEFAULT_CONN_ARGS) {
        return initRequest(connection.conn.post, improveUrl('users'), {
            username,
            password,
            full_name: fullName,
            email,
            jwt_params: jwtParams,
        }, connArgs)
            .then(response => response.data.user)
    },

    /* Change password. */
    changePassword (newPassword, oldPassword, connArgs = DEFAULT_CONN_ARGS) {
        return this.update('users/password', { new_password: newPassword, old_password: oldPassword }, connArgs)
    },

    /* Forgot password.
     * Checks if a user is known by the given email or username. Sends an email with a link to reset the password. */
    forgotPassword (username, email, connArgs = DEFAULT_CONN_ARGS) {
        return initRequest(connection.conn.post, improveUrl('forgot_password'), { username, email }, connArgs)
    },

    /* Recover password */
    recoverPassword (username, recoveryToken, newPassword, connArgs = DEFAULT_CONN_ARGS) {
        return initRequest(connection.conn.post, improveUrl('recover_password'), {
            username,
            recovery_token: recoveryToken,
            new_password: newPassword,
        }, connArgs)
    },

    get (url, data, connArgs) {
        return initRequest(connection.conn.get, improveUrl(url, data), null, connArgs)
    },
    post (url, data, connArgs) {
        return initRequest(connection.conn.post, improveUrl(url), data, connArgs)
    },
    patch (url, data, connArgs) {
        return initRequest(connection.conn.patch, improveUrl(url), data, connArgs)
    },
    delete (url, data, connArgs) {
        return initRequest(connection.conn.delete, improveUrl(url, data), null, connArgs)
    },
    uploadFile (url, data, connArgs) {
        return initRequest(connection.connFile.post, improveUrl(url), data, connArgs)
    },
    uploadFileEmail (url, data, connArgs) {
        return initRequest(connection.connFileEmail.post, improveUrl(url), data, connArgs)
    },
    downloadFile (url, data, connArgs) {
        return initRequest(connection.connFile.get, improveUrl(url, data), null, connArgs)
    },
    create (url, data, connArgs) { return this.post(url, data, connArgs) },
    update (url, data, connArgs) { return this.patch(url, data, connArgs) },
}
