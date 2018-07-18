<template>
    <div>
        done
    </div>
</template>

<script>
import auth from '@/api/auth'

export default {
    created () {
        auth.login('55555555', 'pass')
            .catch(err => console.log(err))
        auth.get('courses')
            .then(resp => {
                if (!resp || resp.length < 4) {
                    console.log('get /courses/ does not work')
                    console.log(resp)
                }
            })
            .catch(resp => console.log(resp))
        auth.get('courses/1')
            .then(resp => {
                if (!resp || resp.name !== 'Is PAV') {
                    console.log('get /courses/1 does not work')
                    console.log(resp)
                }
            })
            .catch(resp => console.log(resp))
        auth.create('courses', {name: 'test', abbr: 'te'})
            .then(resp => {
                if (!resp || resp.description !== 'Succesfully created course.') {
                    console.log('create /courses/ does not work')
                    console.log(resp)
                }
            })
            .catch(resp => console.log(resp))
        auth.update('courses/1', {name: 'Is PAV'})
            .then(resp => {
                if (!resp || resp.name === 'Is PAV') {
                    console.log('update /courses/1 does not work')
                    console.log(resp)
                }
            })
            .catch(resp => console.log(resp))
        auth.get('courses/1/users')
            .then(resp => {
                if (!resp || resp.length < 4 || resp[0].id !== 6) {
                    console.log('get /courses/users does not work')
                    console.log(resp)
                }
            })
            .catch(resp => console.log(resp))
        auth.get('courses/1/roles')
            .then(resp => {
                if (!resp || resp.length <= 3) {
                    console.log('get /courses/1/roles does not work')
                    console.log(resp)
                }
            })
        auth.update('courses/1/roles', {roles: [{
            name: 'Student', can_edit_course: false
        }]})
            .then(resp => {
                resp = resp.result
                if (!resp || resp.length !== 1 || resp[0].can_edit_course !== false) {
                    console.log('patch /courses/1/roles does not work')
                    console.log(resp)
                }
            })
        auth.update('courses/1/roles', {roles: [{
            name: 'Student', can_edit_course: true
        }]})
            .then(resp => {
                resp = resp.result
                if (!resp || resp.length !== 1 || resp[0].can_edit_course !== true) {
                    console.log('patch /courses/1/roles does not work')
                    console.log(resp)
                }
            })
        auth.create('courses/1/roles', {
            name: 'ProStudent' + Math.random(),
            permissions: {can_edit_course: true}
        })
            .then(resp => {
                resp = resp.result
                if (!resp || resp[0].can_edit_course !== true) {
                    console.log('create /courses/1/roles does not work')
                    console.log(resp)
                }
            })
    }
}
</script>
