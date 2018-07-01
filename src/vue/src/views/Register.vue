<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <register-user @handleAction="handleRegistration"/>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import registerUser from '@/components/RegisterUser.vue'

export default {
    name: 'Register',
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'register-user': registerUser
    },
    methods: {
        handleRegistration () {
            this.$router.push({ name: 'Home' })
        }
    }
}
</script>
