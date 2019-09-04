import auth from '@/api/auth.js'

export default {
    grade (data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.create('grades', data, connArgs)
            .then(response => response.data.entry)
    },
    get_history (data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get('grades', data, connArgs)
            .then(response => response.data.grade_history)
    },
}
