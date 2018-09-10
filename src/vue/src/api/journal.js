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

    // /* Get assignment journals.
    //  * Requests all the assignment journals.
    //  * returns a list of all journals.
    //  */
    // update_publish_grades_assignment (aID, published) {
    //     return auth.authenticatedPost('/update_publish_grades_assignment/', {aID: aID, published: published})
    //         .then(response => response.data)
    // },
    //
}
