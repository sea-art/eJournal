<template>
    <content-columns>
        <login-form
            slot="main-content-column"
            @login-succes="handleLoginSucces()"/>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import LoginForm from '@/components/LoginForm.vue'
import loginAPI from '@/api/auth.js'

export default {
    name: 'Login',
    data () {
        return {
        }
    },
    methods: {

    },
    components: {
        'login-form': LoginForm,
        'content-columns': contentColumns
    }
}
</script>
