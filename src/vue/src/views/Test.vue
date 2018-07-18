<template>
    <div>
        done
    </div>
</template>

<script>
import auth from '@/api/auth'

export default {
    created () {
        // auth.login('55555555', 'pass')
        //     .then(resp => console.log(resp))
        //     .catch(err => console.log(err))
        // auth.get('courses')
        //     .then(resp => console.log(resp))
        //     .catch(err => console.log(err))
        // auth.get('courses/1')
        //     .then(resp => console.log(resp))
        //     .catch(err => console.log(err))
        // auth.create('courses', {name: 'test', abbr: 'te'})
        //     .then(resp => console.log(resp))
        //     .catch(err => console.log(err))
        // auth.update('courses/5', {name: 'Is PAV'})
        //     .then(resp => console.log(resp))
        //     .catch(err => console.log(err))
        // auth.delete('courses/14')
        //     .then(resp => console.log(resp))
        //     .catch(err => console.log(err))
        auth.get('courses/1/users')
            .then(resp => console.log(resp))
            .catch(err => console.log(err))
    }
}
</script>
