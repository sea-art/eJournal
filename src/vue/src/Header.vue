<template>
    <div id="header">
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
                                <img src="./assets/ohno.jpeg" class="profile-image"> Engel <b class="caret"></b></a>
                            <!-- <em>User</em> -->
                        </template>
                        <router-link v-if="$route.path != '/'" tag="b-dropdown-item" :to='"/Profile"'>Profile</router-link>
                        <router-link v-if="$route.path != '/'" tag="b-dropdown-item" :to='"/"'>Sign Out</router-link>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<style>
#header {
  background-color: #252C39;
  color: #DEDEDE;
  margin-top: 10px;
}

.profile-image{
    width: 100%;
    max-width: 60px;
    border-radius: 50%;
}
</style>
