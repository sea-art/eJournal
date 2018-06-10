<template>
    <div id="app">
        <Header></Header>
        <div class="container" width="90%">
            <router-view/>
            <b-container class="bv-example-row">
                <b-row class="text-center">
                    <b-col class="p-3 mb-2 bg-primary text-white" cols="3">1/4</b-col>
                    <b-col class="p-3 mb-2 bg-danger text-white" cols="6">2/4 (wider)</b-col>
                    <b-col class="p-3 mb-2 bg-primary text-white" cols="3">1/4</b-col>
                </b-row>
            </b-container>
        </div>
    </div>
</template>

<script>
import Header from '@/Header'

export default {
    name: 'app',
    data () {
        return {}
    },
    components: {
        Header
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

.container {
    min-width: 100%
}
</style>
