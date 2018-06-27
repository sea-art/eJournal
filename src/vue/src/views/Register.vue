<template>
    <content-single-column>
        <register-user @handleAction="handleRegistration"/>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import registerUser from '@/components/RegisterUser.vue'

export default {
    name: 'Register',
    components: {
        'content-single-column': contentSingleColumn,
        'register-user': registerUser
    },
    methods: {
        handleRegistration () {
            // TODO: Handle registratie goed af en redirect naar home page.
            alert('Geregistreerd! :D')
        }
    }
}
</script>
