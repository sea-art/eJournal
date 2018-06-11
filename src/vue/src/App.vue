<template>
    <div id="app">
        <b-container id="main-container">
            <header-bar></header-bar>
            <router-view/>

            <!-- Example of the used grid system. -->
            <b-row>
                <b-col12><h1>Example of the grid system:</h1></b-col12>
            </b-row>
            <b-row>
                <b-col class="p-3 mb-2 bg-primary text-white" cols="3">1/4</b-col>
                <b-col class="p-3 mb-2 bg-danger text-white" cols="6">2/4 (wider)</b-col>
                <b-col class="p-3 mb-2 bg-primary text-white" cols="3">1/4</b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Header from '@/Header'

export default {
    components: {
        'header-bar': Header
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}


.left-content {
    background-color: Blue
}

.main-content {
}

.right-content {
    background-color: Blue
}
</style>
