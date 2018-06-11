<template>
    <b-navbar id="header" toggleable="md">
        <b-navbar-brand :to='"/Home"'>Edag</b-navbar-brand>
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

        <!-- TODO: State-based if statements for display logic. -->
        <b-collapse v-if="$route.path != '/'" is-nav id="nav_collapse">
            <b-navbar-nav>
                <b-nav-item :to='"/Home"'>Courses</b-nav-item>
                <b-nav-item :to='"/Home"'>Assignments</b-nav-item>
            </b-navbar-nav>

            <!-- Right aligned nav items; ml-auto means margin-left:
            auto which aligns an element to the right. -->
            <b-navbar-nav class="ml-auto">
                <b-nav-item-dropdown no-caret right>
                    <img id="nav-profile-image" slot="button-content" src="./assets/ohno.jpeg">
                    <router-link tag="b-dropdown-item" :to='"/Profile"'>Profile</router-link>
                    <router-link tag="b-dropdown-item" :to='"/"'>Sign Out</router-link>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-collapse>

        <b-collapse v-else is-nav id="nav_collapse">
            <b-navbar-nav class="ml-auto">
                <login-inline></login-inline>
            </b-navbar-nav>
        </b-collapse>

    </b-navbar>
</template>

<script>
import LoginInline from '@/components/LoginInline.vue'

export default {
    components: {
        'login-inline': LoginInline
    }
}
</script>

<style>
#header {
  background-color: var(--theme-dark-blue);
}

#nav-profile-image{
    width: 100%;
    max-width: 60px;
    border-radius: 50%;
}
</style>
