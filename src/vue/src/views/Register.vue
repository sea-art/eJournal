<template>
    <content-single-column>
        <register-user/>
    </content-single-column>
</template>

<script>
import contentSingleColumns from '@/components/ContentSingleColumn.vue'
import registerUser from '@/components/RegisterUser.vue'

export default {
    name: 'Register',
    components: {
        'content-single-column': contentSingleColumn,
        'register-user': registerUser
    },
    methods: {
        handleRegistration () {
            alert('Geregistreerd')
        }
    }
}
</script>
