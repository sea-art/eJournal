import auth from '@/api/auth'

export default {
    /* Common file for multi-purpose api calls. */
    get_names (cID = undefined, aID = undefined, jID = undefined, tID = undefined) {
        var data = {}
        if (cID) {
            data.cID = cID
        }

        if (aID) {
            data.aID = aID
        }

        if (jID) {
            data.jID = jID
        }

        if (tID) {
            data.tID = tID
        }

        return auth.authenticatedPost('/get_names/', data)
    }
}
