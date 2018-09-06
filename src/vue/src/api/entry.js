import auth from '@/api/auth'

export default {

    get (id) {
        return auth.get('entries/' + id)
            .then(response => response.data.entry)
    },

    create (data) {
        return auth.create('entries', data)
            .then(response => response.data)
    },

    update (id, data) {
        return auth.update('entries/' + id, data)
            .then(response => response.data.entry)
    },

    delete (id) {
        return auth.delete('entries/' + id)
            .then(response => response.data)
    },

    publish (id, published = true) {
        return auth.update('entries/' + id, {published: published})
            .then(response => response.data.entry)
    }
}
