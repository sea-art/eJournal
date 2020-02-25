import auth from '@/api/auth.js'

export default {
    get (aID, cID = null, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get(`assignments/${aID}`, { course_id: cID }, connArgs)
            .then(response => response.data.assignment)
    },

    create (data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.create('assignments', data, connArgs)
            .then(response => response.data.assignment)
    },

    update (id, data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.update(`assignments/${id}`, data, connArgs)
            .then(response => response.data.assignment)
    },

    delete (aID, cID, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.delete(`assignments/${aID}`, { course_id: cID }, connArgs)
            .then(response => response.data)
    },

    list (cID = null, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get('assignments', { course_id: cID }, connArgs)
            .then(response => response.data.assignments)
    },

    getUpcoming (cID = null, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get('assignments/upcoming', { course_id: cID }, connArgs)
            .then(response => response.data.upcoming)
    },

    getWithLti (id, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get(`assignments/${id}`, { lti: true }, connArgs)
    },

    getImportable (connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get('assignments/importable', null, connArgs)
            .then(response => response.data.data)
    },

    import (id, data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.post(`assignments/${id}/copy/`, data, connArgs)
            .then(response => response.data)
    },
}
