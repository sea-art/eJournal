import auth from '@/api/auth'

export default {

    get (id) {
        return auth.get('comments/' + id)
            .then(response => response.data.comment)
    },

    create (data) {
        return auth.create('comments', data)
            .then(response => response.data.comment)
    },

    update (id, data) {
        return auth.update('comments/' + id, data)
            .then(response => response.data.comment)
    },

    delete (id) {
        return auth.delete('comments/' + id)
            .then(response => response.data)
    },

    getFromEntry (id) {
        return auth.get('comments', {entry_id: id})
            .then(response => response.data.comments)
    }
}
