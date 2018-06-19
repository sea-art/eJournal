<template>
    <b-navbar v-if="!isGuest" id="header" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand :to="'/Home'" class="brand-name">Logboek</b-navbar-brand>

        <b-navbar-toggle class="ml-auto mr-auto" target="nav_collapse" aria-expanded="false" aria-controls="nav_collapse">
            <span class="nav_collapse__icon nav_collapse__icon--open">
                <icon class="collapse-icon" name="caret-down" scale="1.75"></icon>
            </span>
            <span class="nav_collapse__icon nav_collapse__icon--close">
                <icon class="collapse-icon" name="caret-up" scale="1.75"></icon>
            </span>
        </b-navbar-toggle>

        <b-collapse is-nav id="nav_collapse">
            <b-navbar-nav class="mr-auto">
                <b-nav-item :to="{ name : 'Home' }">Courses</b-nav-item>
                <b-nav-item :to="{ name : 'AssignmentsOverview' }">Assignments</b-nav-item>
            </b-navbar-nav>
        </b-collapse>

        <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown no-caret right id="nav-dropdown-options">
                <img id="nav-profile-image" slot="button-content" src="/static/oh_no/ohno.jpeg">
                <b-nav-dropdown-item><b-button :to="{ name: 'Profile'}">Profile</b-button></b-nav-dropdown-item>
                <b-nav-dropdown-item><b-button @click="handleLogout()">Sign out</b-button><br/></b-nav-dropdown-item>
            </b-nav-item-dropdown>
        </b-navbar-nav>
    </b-navbar>

    <b-navbar v-else id="header" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand  :to="'/'" class="brand-name">Logboek</b-navbar-brand>

        <b-navbar-nav class="ml-auto">
            <b-nav-dropdown right no-caret id="nav-dropdown-options">
                <img id="nav-profile-image" slot="button-content" src="~@/assets/unknown-profile.png">
                <div><login-form @login-succes="handleLoginSucces()"/></div>
            </b-nav-dropdown>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    components: {
        'login-form': LoginForm,
        icon
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
            alert('Handle logout')
            this.isGuest = true
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

#nav-dropdown-options a {
    padding: 0px !important;
}

#nav-dropdown-options a.btn {
    padding: 0.375rem 0.75rem !important;
}

#nav_collapse {
    background-color: var(--theme-dark-blue);
}

.collapse-icon {
    fill: white !important;
}

/* Handles rotation of the arrow icon. */
[aria-expanded="false"] .nav_collapse__icon--open {
    display: block;
}

[aria-expanded="false"] .nav_collapse__icon--close {
    display: none;
}

[aria-expanded="true"] .nav_collapse__icon--open {
    display: none;
}

[aria-expanded="true"] .nav_collapse__icon--close {
    display: block;
}

#login-form {
    background: none !important;
}

.dropdown-menu {
    background: var(--theme-light-grey) !important;
    border: none !important;
    padding: 5px;
    margin-top: 10px;
}

.dropdown-menu .btn {
    width: 100%;
    text-align: left;
}

.brand-name {
    font-weight: bold;
    font-size: 25px;
}

#nav-profile-image{
    width: 50px;
    height: 50px;
    border-radius: 50% !important;
}

@media(max-width:992px){
    #nav-dropdown-options {
        position: absolute;
        top: 10px;
        right: 10px;
        width: auto;
    }

    #nav-dropdown-options a.nav-link {
        text-align: right !important;
    }

    #header {
        min-height: 70px;
        height: auto;
    }

    .navbar-toggler {
        position: absolute;
        left: 50%;
        right: 50%;
        top: 15px;
        border-radius: 50% !important;
    }
}
</style>
