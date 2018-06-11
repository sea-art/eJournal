<template>
    <div id="app">
        <header-bar></header-bar>
        <router-view/>
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
:root {
    --theme-dark-blue: #252C39;
    --theme-peach: #E9A480;
    --theme-light-grey: #EDEDED;
    --theme-dark-grey: #DDDDDD;
    --theme-pink: #E64769;
    --theme-blue: #22648A;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

.left-content {
}

.main-content {
    background-color: var(--theme-dark-grey);
}

.right-content {
}

</style>
