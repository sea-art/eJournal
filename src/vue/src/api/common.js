import auth from '@/api/auth'

export default {
    /* Common file for multi-purpose api calls. */
    get_names (data) {
        return auth.authenticatedPost('/get_names/', data).then(response => response.data)
    }
}
