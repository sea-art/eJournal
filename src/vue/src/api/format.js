import auth from '@/api/auth'

export default {
    update_format (fID, templates, presets) {
        return auth.authenticatedPost('/update_format/', {fID: fID, templates: templates, presets: presets})
            .then(response => response.data)
    }
}
