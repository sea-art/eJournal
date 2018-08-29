import auth from '@/api/auth'

export default {

    get (id) {
        return auth.get('journalformats')
            .then(response => response.data.format)
    },

    update (id, data = null) {
        return auth.update('journalformats/' + id, data)
            .then(response => response.data.format)
    }

    // create_template (name, fields) {
    //     return auth.authenticatedPost('/create_template/', {name: name, fields: fields})
    //         .then(response => response.data)
    // },
    //
    // get_format (aID) {
    //     return auth.authenticatedGet('/get_format/' + aID + '/')
    //         .then(response => response.data)
    // },
    //
    // update_format (aID, templates, maxPoints, presets, unusedTemplates, removedTemplates, removedPresets) {
    //     return auth.authenticatedPost('/update_format/', {aID: aID, templates: templates, max_points: maxPoints, presets: presets, unused_templates: unusedTemplates, removed_templates: removedTemplates, removed_presets: removedPresets})
    //         .then(response => response.data)
    // },
}
