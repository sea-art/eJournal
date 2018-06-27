<template>
    <div>
        <register-user @handleAction="handleRegistered" :lti="lti"/>
    </div>
</template>

<script>
import registerUser from '@/components/RegisterUser.vue'

export default {
    name: 'CreateUser',
    props: ['lti'],
    components: {
        'register-user': registerUser
    },
    methods: {
        handleRegistered () {
            this.$emit('handleAction')
        }
    }
}
</script>
