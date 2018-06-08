<template>
    <div id="app">
        <div id="header">
            <!-- Place holder image -->
            <img src="./assets/logo.png">
            <!-- Redirection buttons, only visible dependent on current router path -->

            <b-navbar toggleable="md" type="dark" variant="info">
                <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
                <b-navbar-brand href="#">NavBar</b-navbar-brand>

                <b-collapse is-nav id="nav_collapse">
                    <b-navbar-nav>
                        <router-link tag="b-nav-item" to="/">Homepage</router-link>
                        <router-link v-if="$route.path != '/'" tag="b-nav-item" :to='"/Profile"'>Profile</router-link>
                        <router-link v-if="$route.params.course != undefined" tag="b-nav-item" :to='"/Dashboard"'>Courses</router-link>
                        <router-link v-if="$route.params.assign != undefined" tag="b-nav-item" :to='"/Dashboard/"+$route.params.course'>{{$route.params.course}}</router-link>
                        <router-link v-if="$route.params.student != undefined" tag="b-nav-item" :to='"/Dashboard/"+$route.params.course+"/"+$route.params.assign'>{{$route.params.assign}}</router-link>

                        <!-- <b-nav-item href="/Profile">Link</b-nav-item> -->
                        <!-- <b-nav-item href="#" disabled>Disabled</b-nav-item> -->
                    </b-navbar-nav>

                    <!-- Right aligned nav items -->
                    <b-navbar-nav class="ml-auto">
                        <b-nav-item-dropdown right>
                            <!-- Using button-content slot -->
                            <template slot="button-content">
                            <em>User</em>
                            </template>
                            <b-dropdown-item href="#">Profile</b-dropdown-item>
                            <b-dropdown-item href="#">Signout</b-dropdown-item>
                        </b-nav-item-dropdown>
                    </b-navbar-nav>
                </b-collapse>
            </b-navbar>

            <!-- <b-row class="text-center">
                <router-link tag="b-button" to="/">Homepage</router-link>
                <router-link v-if="$route.path != '/'" tag="b-button" :to='"/Profile"'>Profile</router-link>
                <router-link v-if="$route.params.course != undefined" tag="b-button" :to='"/Courses"'>Courses</router-link>
                <router-link v-if="$route.params.assign != undefined" tag="b-button" :to='"/Courses/"+$route.params.course'>{{$route.params.course}}</router-link>
                <router-link v-if="$route.params.student != undefined" tag="b-button" :to='"/Courses/"+$route.params.course+"/"+$route.params.assign'>{{$route.params.assign}}</router-link>
            </b-row> -->

        </div>
        <div class="container" width="90%">
            <router-view/>
        </div>
    </div>

</template>

<script>
export default {
    name: 'app',
    data () {
        return {}
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;

  margin-top: 10px;
}

#header {
  background-color: #252C39;
  color: #DEDEDE;
  margin-top: 10px;
}
</style>
