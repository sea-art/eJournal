<template>
    <div id="header">
        <!-- Place holder image -->
        <img src="./assets/logo.png">
        <!-- Redirection buttons, only visible dependent on current router path -->

        <b-navbar toggleable="md" type="light" variant="info">
            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
            <b-navbar-brand :to='"/"'>Edag</b-navbar-brand>

            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav>
                    <b-nav-item v-if="$route.path != '/'" :to='"/Dashboard"'>Courses</b-nav-item>
                    <b-nav-item v-if="$route.path != '/'" :to='"/Dashboard"'>Assignments</b-nav-item>
                    <!-- <b-nav-item v-if="$route.path != '/'" tag="b-nav-item" :to='"/Dashboard/"+$route.params.course'>{{$route.params.course}}</b-nav-item> -->
                    <!-- <b-nav-item v-if="$route.params.student != undefined" tag="b-nav-item" :to='"/Dashboard/"+$route.params.course+"/"+$route.params.assign'>{{$route.params.assign}}</b-nav-item> -->
                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-nav-item-dropdown right v-if="$route.path != '/'">
                        <!-- Using button-content slot -->
                        <template slot="button-content">
                        <em>User</em>
                        </template>
                        <router-link v-if="$route.path != '/'" tag="b-dropdown-item" :to='"/Profile"'>Profile</router-link>
                        <router-link v-if="$route.path != '/'" tag="b-dropdown-item" :to='"/"'>Sign Out</router-link>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

// <script>
// export default {
//     name: 'app',
//     data () {
//         return {}
//     },
// }
// </script>

<style>
#header {
  background-color: #252C39;
  color: #DEDEDE;
  margin-top: 10px;
}
</style>
