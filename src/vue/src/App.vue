<template>
    <div id="app">
        <div id="header">
            <!-- Place holder image -->
            <img src="./assets/logo.png">
            <!-- Redirection buttons, only visible dependent on current router path -->
            <router-link tag="button" to="/">Homepage</router-link>
            <router-link v-if="$route.path != '/'" tag="button" :to='"/Profile"'>Profile</router-link>
            <router-link v-if="$route.params.course != undefined" tag="button" :to='"/Courses"'>Courses</router-link>
            <router-link v-if="$route.params.assign != undefined" tag="button" :to='"/Courses/"+$route.params.course'>{{$route.params.course}}</router-link>
            <router-link v-if="$route.params.student != undefined" tag="button" :to='"/Courses/"+$route.params.course+"/"+$route.params.assign'>{{$route.params.assign}}</router-link>
        </div>
        <div class="container">
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
