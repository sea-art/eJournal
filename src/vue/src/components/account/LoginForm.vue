<template>
    <b-card class="blue-border no-hover card-last-elem-button">
        <b-form @submit.prevent="handleLogin()">
            <b-input class="multi-form theme-input" v-model="username" required placeholder="Username"/>
            <b-input class="multi-form theme-input" type="password" @keyup.enter="handleLogin()" v-model="password" required placeholder="Password"/>
            <b-button class="float-right multi-form" type="submit">
                <icon name="sign-in"/>
                Log in
            </b-button>
        </b-form>
    </b-card>
</template>

<script>
import authAPI from '@/api/auth'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LoginForm',
    data () {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        handleLogin () {
            authAPI.login(this.username, this.password)
                .then(_ => { this.$emit('handleAction') })
                .catch(_ => { this.$toasted.error('Could not login') })
        }
    },
    components: {
        'icon': icon
    }
}
</script>
