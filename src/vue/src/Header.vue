<template>
    <!-- Section visible if user logged in -->
    <b-navbar v-if="loggedIn" id="header" class="shadow" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand :to="{ name: 'Home' }" class="brand-name"><span>e</span>Journal</b-navbar-brand>

        <b-navbar-toggle class="ml-auto mr-auto" target="nav-collapse" aria-expanded="false" aria-controls="nav-collapse">
            <span class="nav-collapse__icon nav-collapse__icon--open">
                <icon class="collapse-icon" name="caret-down" scale="1.75"/>
            </span>
            <span class="nav-collapse__icon nav-collapse__icon--close">
                <icon class="collapse-icon" name="caret-up" scale="1.75"/>
            </span>
        </b-navbar-toggle>

        <b-collapse is-nav id="nav-collapse">
            <b-navbar-nav class="mr-auto">
                <b-nav-item :to="{ name : 'Home' }">Courses</b-nav-item>
                <b-nav-item :to="{ name : 'AssignmentsOverview' }">Assignments</b-nav-item>
            </b-navbar-nav>
        </b-collapse>

        <b-navbar-nav class="ml-auto">
            <b-nav-item :to="{ name : 'Feedback' }">Feedback</b-nav-item>
            <b-nav-dropdown no-caret right id="nav-dropdown-options">
                <div class="profile-picture-container" slot="button-content">
                    <img class="profile-picture" :src="profileImg">
                </div>
                <b-button :to="{ name: 'Profile' }" class="multi-form">
                    <icon name="user"/>
                    &nbsp;Profile
                </b-button>
                <b-button :to="{ name: 'Logout' }">
                    <icon name="sign-out"/>
                    Log out
                </b-button>
            </b-nav-dropdown>
        </b-navbar-nav>
    </b-navbar>

    <!-- Section visible if user logged out -->
    <b-navbar v-else id="header" class="shadow" toggleable="md" type="dark" fixed=top>
        <b-navbar-brand  :to="{ name: 'Guest' }" class="brand-name"><span>e</span>Journal</b-navbar-brand>

        <b-navbar-nav class="ml-auto">
            <b-nav-dropdown right no-caret id="nav-dropdown-options" ref="loginDropdown">
                <div class="profile-picture-container bg-white d-flex justify-content-center align-items-center" slot="button-content">
                    <icon name="user" scale="2.5"/>
                </div>
                <b-button class="multi-form" :to="{ name: 'Register' }">
                    <icon name="user-plus"/>
                    Register
                </b-button>
                <b-button :to="{ name: 'Login' }">
                    <icon name="sign-in"/>
                    Log in
                </b-button>
            </b-nav-dropdown>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import { mapGetters } from 'vuex'

export default {
    components: {
        icon
    },
    data () {
        return {
            defaultProfileImg: '/static/unknown-profile.png'
        }
    },
    computed: {
        ...mapGetters({
            loggedIn: 'user/loggedIn',
            profileImg: 'user/profilePicture'
        })
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
    .brand-name
        font-weight: bold
        font-size: 25px
        span
            color: $theme-blue !important
    .navbar-toggler
        .collapse-icon
            fill: white !important
        @include md-max
            position: absolute
            left: 50%
            right: 50%
            top: 15px
            transform: translateX(-50%)
            border-radius: 50% !important
    /* Handles rotation of the arrow icon. */
    [aria-expanded="false"] .nav-collapse__icon--open
        display: block

    [aria-expanded="false"] .nav-collapse__icon--close
        display: none

    [aria-expanded="true"] .nav-collapse__icon--open
        display: none

    [aria-expanded="true"] .nav-collapse__icon--close
        display: block
    @include md-max
        min-height: 70px
        height: auto

#nav-dropdown-options
    .profile-picture-container
        border-radius: 50% !important
        width: 50px
        height: 50px
        @include md-max
            position: absolute
            top: 10px
            right: 10px
    a
        padding: 0px !important
    a.btn
        padding: 0.375rem 0.75rem !important
        width: 100%
    @include md-max
        position: absolute
        top: 0px
        right: 0px
        width: auto

        a.nav-link
            text-align: right !important

#nav-collapse
    background-color: $theme-dark-blue

.dropdown-menu
    background: $theme-dark-grey !important
    border: none !important
    padding: 10px 5px
    margin-top: 10px
    .btn
        justify-content: left
        svg
            margin-left: 0px
    @include md-max
        margin-top: 70px
</style>
