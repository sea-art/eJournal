<template>
    <b-navbar id="header" toggleable="md" v-if="$route.path != '/'">
            <b-navbar-brand :to='"/"'>Edag</b-navbar-brand>
            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav>
                    <b-nav-item v-if="$route.path != '/'" :to='"/Home"'>Courses</b-nav-item>
                    <b-nav-item v-if="$route.path != '/'" :to='"/Home"'>Assignments</b-nav-item>
                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <!-- TODO: State-based if statements for display logic. -->
                    <b-nav-item-dropdown right v-if="$route.path != '/'">
                        <img id="nav-profile-image" slot="button-content" src="./assets/ohno.jpeg">
                        <router-link v-if="$route.path != '/'" tag="b-dropdown-item" :to='"/Profile"'>Profile</router-link>
                        <router-link v-if="$route.path != '/'" tag="b-dropdown-item" :to='"/"'>Sign Out</router-link>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
</template>

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
