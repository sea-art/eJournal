<template>
    <!-- Section visible if user logged in -->
    <b-navbar v-if="$root.validToken" id="header" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand :to="{ name: 'Home' }" class="brand-name"><span>e</span>Journal</b-navbar-brand>

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

    <!-- Section visible if user logged out -->
    <b-navbar v-else id="header" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand  :to="{ name: 'Guest' }" class="brand-name"><span>e</span>Journal</b-navbar-brand>

        <b-navbar-nav class="ml-auto">
            <b-nav-dropdown right no-caret id="nav-dropdown-options" ref="loginDropdown">
                <img id="nav-profile-image" slot="button-content" :src="profileImg">
                <b-button class="login-form-header" :to="{ name: 'Register' }">Sign Up!</b-button>
                <b-button class="login-form-header" :to="{ name: 'Login' }">Login</b-button>
            </b-nav-dropdown>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import auth from '@/api/auth.js'

export default {
    components: {
        icon
    },
    data () {
        return {
            defaultProfileImg: '../static/unknown-profile.png',
            profileImg: '',
            username: '',
            password: '',
            profile: '',
            profileFetchAttempts: 0
        }
    },
    watch: {
        '$root.validToken': function (validToken) {
            this.setProfileImg()
            if (!validToken) {
                this.profileImg = this.defaultProfileImg
            } else {
                this.setUserProfile()
            }
        }
    },
    methods: {
        setUserProfile () {
            auth.get('users/0')
                .then(user => {
                    this.profile = user
                    this.setProfileImg()
                })
                .catch(_ => {
                    this.$toasted.error('Something went wrong retrieving user data')
                })
        },
        setProfileImg () {
            /* Sets the profile img if found, else a default is set.
             * If a valid token is registered but no profile image is found,
             * one more call is made to retrieve the profile image. */
            if (this.$root.validToken) {
                if (this.profile.picture) {
                    this.profileImg = this.profile.picture
                } else if (this.profileFetchAttempts === 0) {
                    this.setUserProfile()
                    this.profileFetchAttempts = this.profileFetchAttempts + 1
                } else {
                    this.profileImg = this.defaultProfileImg
                    this.profileFetchAttempts = 0
                }
            } else {
                this.profileImg = this.defaultProfileImg
            }
        }
    },
    created () {
        this.setProfileImg()
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/modules/breakpoints.sass'

#header
    background-color: $theme-dark-blue
    color: white
    font-family: 'Roboto Condensed', sans-serif
    font-size: 1.3em
    height: 70px
    @include md-max
        min-height: 70px
        height: auto

#nav-dropdown-options
    @include md-max
        position: absolute
        top: 10px
        right: 10px
        width: auto

        a.nav-link
            text-align: right !important

#nav-dropdown-options a
    padding: 0px !important

#nav-dropdown-options a.btn
    padding: 0.375rem 0.75rem !important

#nav-collapse
    background-color: $theme-dark-blue

.collapse-icon
    fill: white !important

/* Handles rotation of the arrow icon. */
[aria-expanded="false"] .nav-collapse__icon--open
    display: block

[aria-expanded="false"] .nav-collapse__icon--close
    display: none

[aria-expanded="true"] .nav-collapse__icon--open
    display: none

[aria-expanded="true"] .nav-collapse__icon--close
    display: block

.dropdown-menu
    background: $theme-light-grey !important
    border: none !important
    padding: 5px
    margin-top: 10px

.dropdown-menu .btn
    width: 100%
    text-align: left

.brand-name
    font-weight: bold
    font-size: 25px

.brand-name span
    color: $theme-blue !important

#nav-profile-image
    width: 50px
    height: 50px
    border-radius: 50% !important

.login-form-header
    background-color: $theme-light-grey

.navbar-toggler
    @include md-max
        position: absolute
        left: 50%
        right: 50%
        top: 15px
        transform: translateX(-50%)
        border-radius: 50% !important
</style>
