<template>
    <div>
        <register-user :lti="lti"/>
    </div>
</template>

<script>
import registerUser from '@/components/RegisterUser.vue'
import userApi from '@/api/user.js'

export default {
    name: 'CreateUser',
    props: ['lti'],
    components: {
        'register-user': registerUser
    },
    methods: {
        handleCreated () {

        }
    }
}
</script>
