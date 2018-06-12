<template>
    <div id="app">
        <header-bar/>
        <router-view style="height: 100%"/>
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
    --theme-light-grey: #EEEEEE;
    --theme-dark-grey: #BBBBBB;
    --theme-pink: #E64769;
    --theme-blue: #22648A;
    --theme-red: #c83b4b;
    --theme-medium-grey: #DEDEDE;
}

* {
    border-radius: 0px !important;
    text-decoration: none !important;
    color: var(--theme-dark-blue);
}

#app {
    overflow-x: hidden;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}

.left-content {
}

.main-content {
    padding-left: 0px;
    padding-right: 0px;
    background-color: var(--theme-medium-grey);
}

.right-content {

}

</style>
