<template>
    <div id="app">
        <header-bar/>
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
    text-align: left;
}

@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700');

#app {
    overflow-x: hidden;
    font-family: 'Roboto', sans-serif;
    font-size: 20px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}

h1 {
    font-weight: bold;
    font-size: 60px;
    border-left: 20px solid var(--theme-dark-blue);
    padding-left: 20px;
}

h2 {
    font-weight: bold;
    font-size: 35px;
}

h3 {
    font-weight: bold;
    font-size: 35px;
    border-left: 20px solid var(--theme-dark-blue);
    padding-left: 20px;
}

h4 {
    font-weight: bold;
    font-size: 30px;
    color: var(--theme-blue);
    border-left: 20px solid var(--theme-dark-blue);
    padding-left: 20px;
}

h5 {
    font-size: 30px;
}

h6 {
    font-size: 20px;
    color: var(--theme-blue);
}

.button {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 25px;
}

.left-content {
}

.main-content {
    padding-top: 40px;
    padding-left: 0px;
    padding-right: 0px;
    background-color: var(--theme-medium-grey);
}

.right-content {
}

</style>
