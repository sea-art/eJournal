import auth from '@/api/auth'

export default {

    create (data) {
        return auth.create('groups', data)
            .then(response => response.data.group)
    },

    update (id, data) {
        return auth.update('groups/' + id, data)
            .then(response => response.data.group)
    },

    delete (cID, groupName) {
        return auth.delete('groups/' + cID, {group_name: groupName})
            .then(response => response.data)
    },

    getAllFromCourse (cID) {
        if (cID) {
            return auth.get('groups', {course_id: cID})
                .then(response => response.data.groups)
        }
        return auth.get('groups')
            .then(response => response.data.groups)
    }
}
