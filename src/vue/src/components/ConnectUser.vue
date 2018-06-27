<template>
    <div>
        <login-form/>
    </div>
</template>

<script>
import loginForm from '@/components/LoginForm.vue'

export default {
    name: 'ConnectUser',
    components: {
        'login-form': loginForm
    },
    methods: {
        connectCourse (cID) {
            courseApi.connect_course_lti(cID, this.lti.ltiCourseID)
                .then(response => { this.$emit('handleAction', response.cID) })
        }
    },
}
</script>
