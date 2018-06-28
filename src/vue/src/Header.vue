<template>
    <b-navbar v-if="$root.validToken" id="header" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand :to="'/Home'" class="brand-name"><span>e</span>Journal</b-navbar-brand>

        <b-navbar-toggle class="ml-auto mr-auto" target="nav-collapse" aria-expanded="false" aria-controls="nav-collapse">
            <span class="nav-collapse__icon nav-collapse__icon--open">
                <icon class="collapse-icon" name="caret-down" scale="1.75"></icon>
            </span>
            <span class="nav-collapse__icon nav-collapse__icon--close">
                <icon class="collapse-icon" name="caret-up" scale="1.75"></icon>
            </span>
        </b-navbar-toggle>

        <b-collapse is-nav id="nav-collapse">
            <b-navbar-nav class="mr-auto">
                <b-nav-item :to="{ name : 'Home' }">Courses</b-nav-item>
                <b-nav-item :to="{ name : 'AssignmentsOverview' }">Assignments</b-nav-item>
            </b-navbar-nav>
        </b-collapse>

        <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown no-caret right id="nav-dropdown-options">
                <img id="nav-profile-image" slot="button-content" :src="profileImg">
                <b-dropdown-item><b-button :to="{ name: 'Profile' }" class="multi-form">Profile</b-button></b-dropdown-item>
                <b-dropdown-item><b-button :to="{ name: 'Logout' }">Sign out</b-button><br/></b-dropdown-item>
            </b-nav-item-dropdown>
        </b-navbar-nav>
    </b-navbar>

    <b-navbar v-else id="header" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand  :to="'/'" class="brand-name"><span>e</span>Journal</b-navbar-brand>

        <b-navbar-nav class="ml-auto">
            <b-nav-dropdown right no-caret id="nav-dropdown-options" ref="loginDropdown">
                <!-- TODO Fix dynamic binding default image -->
                <img id="nav-profile-image" slot="button-content" src="~@/assets/unknown-profile.png">

                <b-form @submit.prevent="handleLogin()" class="login-form-header">
                    <b-input class="multi-form" v-model="username" required placeholder="Username"/>
                    <b-input class="multi-form" type="password" @keyup.enter="handleLogin()" v-model="password" required placeholder="Password"/>
                    <b-button class="multi-form" type="submit">Login</b-button><br/>
                    <b-button>Forgot password?</b-button>
                </b-form>

            </b-nav-dropdown>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import authAPI from '@/api/auth.js'
import userAPI from '@/api/user.js'

export default {
    components: {
        icon
    },
    data () {
        return {
            // TODO Figure out why webpack messes this up
            profileImg: '~/assets/unknown-profile.png',
            username: '',
            password: '',
            profile: ''
        }
    },
    methods: {
        handleLogout () {
            authAPI.logout()
            this.$router.push('/')
        },
        handleLogin () {
            authAPI.login(this.username, this.password)
                .then(_ => {
                    console.log('Handling login success')
                    this.setProfilePicture()
                    this.$router.push({name: 'Home'})
                })
                .catch(_ => {
                    this.$toasted.error('Could not login')
                })
        },
        setProfilePicture () {
            userAPI.getOwnUserData()
                .then(user => {
                    this.profile = user
                    if (user.picture) {
                        this.profileImg = user.picture
                    } else {
                        // TODO Set default user picture
                    }
                })
                .catch(_ => {
                    this.$toasted.error('Something went wrong retrieving user data')
                    // TODO Set default user picture
                })
        }
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

#nav-collapse {
    background-color: var(--theme-dark-blue);
}

.collapse-icon {
    fill: white !important;
}

/* Handles rotation of the arrow icon. */
[aria-expanded="false"] .nav-collapse__icon--open {
    display: block;
}

[aria-expanded="false"] .nav-collapse__icon--close {
    display: none;
}

[aria-expanded="true"] .nav-collapse__icon--open {
    display: none;
}

[aria-expanded="true"] .nav-collapse__icon--close {
    display: block;
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

.brand-name span {
    color: var(--theme-blue) !important;
}

#nav-profile-image {
    width: 50px;
    height: 50px;
    border-radius: 50% !important;
}

.login-form-header {
    background-color: var(--theme-light-grey);
}

@media(max-width:992px) {
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
        transform: translateX(-50%);
        border-radius: 50% !important;
    }
}
</style>
