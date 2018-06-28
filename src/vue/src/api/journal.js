import auth from '@/api/auth'

export default {
    /* Get assignment journals.
     * Requests all the assignment journals.
     * returns a list of all journals.
     */
    get_assignment_journals (aID) {
        return auth.authenticatedGet('/get_assignment_journals/' + aID + '/')
            .then(response => response.data)
            .catch(error => { throw error })
    },

    get_nodes (jID) {
        return auth.authenticatedGet('/get_nodes/' + jID + '/')
            .then(response => response.data)
    },

    create_entry (jID, tID, content, nID = undefined) {
        var data = {tID: tID, jID: jID, content: content}
        if (nID) {
            data.nID = nID
        }

        return auth.authenticatedPost('/create_entry/', data)
            .then(response => response.data)
    },

    create_template (name, fields) {
        return auth.authenticatedPost('/create_template/', {name: name, fields: fields})
            .then(response => response.data)
    },

    get_format (aID) {
        return auth.authenticatedGet('/get_format/' + aID + '/')
            .then(response => response.data)
    },

    update_format (aID, templates, presets, unusedTemplates, removedTemplates, removedPresets) {
        return auth.authenticatedPost('/update_format/', {aID: aID, templates: templates, presets: presets, unused_templates: unusedTemplates, removed_templates: removedTemplates, removed_presets: removedPresets})
            .then(response => response.data)
    },

    update_grade_entry (eID, grade, published) {
        return auth.authenticatedPost('/update_grade_entry/' + eID + '/', {grade: grade, published: published})
            .then(response => response.data)
    },

    update_publish_grade_entry (eID, published) {
        return auth.authenticatedPost('/update_publish_grade_entry/' + eID + '/', {published: published})
            .then(response => response.data)
    },

    update_publish_grades_assignment (aID, published) {
        return auth.authenticatedPost('/update_publish_grades_assignment/' + aID + '/', {published: published})
            .then(response => response.data)
    },

    update_publish_grades_journal (jID, published) {
        return auth.authenticatedPost('/update_publish_grades_journal/' + jID + '/', {published: published})
            .then(response => response.data)
    }
}
