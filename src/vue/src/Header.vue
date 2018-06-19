<template>
    <b-navbar id="header" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand v-if="isGuest" :to="'/'" class="brand-name">Logboek</b-navbar-brand>
        <b-navbar-brand v-else :to="'/Home'" class="brand-name">Logboek</b-navbar-brand>

        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

        <b-collapse is-nav id="nav_collapse">
            <b-navbar-nav v-if="!isGuest">
                <b-nav-item :to="{ name : 'Home' }">Courses</b-nav-item>
                <b-nav-item :to="{ name : 'AssignmentsOverview' }">Assignments</b-nav-item>
            </b-navbar-nav>
            <b-nav-dropdown v-if="!isGuest" class="ml-auto" right no-caret id="nav-dropdown-options">
                <img id="nav-profile-image" slot="button-content" src="/static/oh_no/ohno.jpeg">
                <b-button :to="{ name: 'Profile'}">Profile</b-button>
                <b-button @click="handleLogout()">Sign out</b-button><br/>
            </b-nav-dropdown>
            <b-nav-dropdown v-if="isGuest" class="ml-auto" right no-caret id="nav-dropdown-options-guest">
                <img id="nav-profile-image" slot="button-content" src="~@/assets/unknown-profile.png">
                <login-form @login-succes="handleLoginSucces()"/>
            </b-nav-dropdown>
        </b-collapse>
    </b-navbar>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue'
import loginAPI from '@/api/auth.js'

export default {
    components: {
        'login-form': LoginForm
    },
    data () {
        return {
            // TODO Figure out why webpack messes this up
            profileImg: '~@/assets/unknown-profile.png',
            isGuest: true
        }
    },
    methods: {
        checkPermissions () {
            this.isGuest = this.$router.currentRoute.path === '/'
        },
        handleLogout () {
            this.isGuest = true
            loginAPI.logout()
            this.$router.push('/')
        },
        handleLoginSucces () {
            this.isGuest = false
            // this.$root.$emit('bv::toggle::collapse', 'nav_collapse')
            this.show = false
            this.$nextTick(() => { this.show = true })
            this.$router.push('/Home')
        }
    },
    created () {
        this.checkPermissions()
    }
}
</script>

<style>
#header {
    background-color: var(--theme-dark-blue);
    color: var(--theme-pink);
    font-family: 'Roboto Condensed', sans-serif;
    height: 70px;
}

#nav_collapse {
    background-color: var(--theme-dark-blue);
}

#nav-dropdown-options a {
    padding: 0px !important;
}

.dropdown-menu {
    background: none !important;
}

.brand-name {
    font-weight: bold;
    font-size: 25px;
}

#nav-profile-image{
    width: 50px;
    height: 50px;
    border-radius: 50% !important;
    margin-left: 20px;
}
</style>
