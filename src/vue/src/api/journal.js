import auth from '@/api/auth'

export default {

    get (id) {
        return auth.get('journals/' + id)
            .then(response => response.data.journal)
    },

    create (data) {
        return auth.create('journals', data)
            .then(response => response.data.journal)
    },

    update (id, data = null) {
        return auth.update('journals/' + id, data)
            .then(response => response.data.journal)
    },

    delete (id) {
        return auth.delete('journals/' + id)
            .then(response => response.data)
    },

    getNodes (id) {
        return auth.get('nodes', {journal_id: id})
            .then(response => response.data.nodes)
    },

    getFromAssignment (id) {
        return auth.get('journals', {assignment_id: id})
            .then(response => response.data.journals)
    }
}
