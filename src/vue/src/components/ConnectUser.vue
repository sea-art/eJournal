<template>
    <div>
        <login-form @handleAction="connectUser"/>
    </div>
</template>

<script>
import loginForm from '@/components/LoginForm.vue'
import userApi from '@/api/user.js'

export default {
    name: 'ConnectUser',
    props: ['lti'],
    components: {
        'login-form': loginForm
    },
    methods: {
        connectUser (uID) {
            userApi.updateLtiIdToUser(lti.ltiJWT)
                .then(response => { this.$emit('handleAction') })
        }
    },
}
</script>
