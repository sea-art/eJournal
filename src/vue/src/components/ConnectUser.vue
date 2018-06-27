<template>
    <div>
        <login-form @handleAction="connectUser"/>
    </div>
</template>

<script>
import loginForm from '@/components/LoginForm.vue'

export default {
    name: 'ConnectUser',
    props: ['lti'],
    components: {
        'login-form': loginForm
    },
    methods: {
        connectUser (uID) {
            courseApi.connect_course_lti(cID, this.lti.ltiCourseID)
                .then(response => { this.$emit('handleAction', response.cID) })
        }
    },
}
</script>
