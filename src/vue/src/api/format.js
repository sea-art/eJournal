import auth from '@/api/auth'

export default {

    get (id) {
        return auth.get('formats/' + id)
            .then(response => response.data)
    },

    update (id, data = null) {
        return auth.update('formats/' + id, data)
            .then(response => response.data)
    }

    // create_template (name, fields) {
    //     return auth.authenticatedPost('/create_template/', {name: name, fields: fields})
    //         .then(response => response.data)
    // }
}
