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
    }

    // /* Create Entry Comment with given text, author and entry.
    //    Decide wether to publish straight away based on the current state
    //    of the grade corresponding to the entry. */
    // createEntryComment (eID, uID, text, entryGradePublished, publishAfterGrade) {
    //     return auth.authenticatedPost('/create_entrycomment/', {
    //         eID: eID,
    //         uID: uID,
    //         text: text,
    //         published: entryGradePublished || !publishAfterGrade
    //     })
    //         .then(response => response.data.comment)
    // },
    //
    // /* Update Entry Comment with given text and EntryComment. */
    // updateEntryComments (ecID, text) {
    //     return auth.authenticatedGet('/update_entrycomments/', { ecID: ecID, text: text })
    //         .then(response => response.data)
    // }
}
