import auth from '@/api/auth'

export default {
    create (data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.create('groups', data, connArgs)
            .then(response => response.data.group)
    },

    update (id, data, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.update('groups/' + id, data, connArgs)
            .then(response => response.data.group)
    },

    delete (id, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.delete('groups/' + id, null, connArgs)
    },

    getAllFromCourse (cID, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get('groups', {course_id: cID}, connArgs)
            .then(response => response.data.groups)
    },

    getDataNose (cID, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get('groups/datanose', {course_id: cID}, connArgs)
            .then(response => response.data.groups)
    },

    getMembers (gID, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.get('members', {group_id: gID}, connArgs)
            .then(response => response.data.members)
    },

    removeMember (gID, uID, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.delete('members/' + gID, {user_id: uID}, connArgs)
            .then(response => response.data.participants)
    },

    addMember (gID, uID, connArgs = auth.DEFAULT_CONN_ARGS) {
        return auth.create('members', {group_id: gID, user_id: uID}, connArgs)
            .then(response => response.data.participants)
    }
}
