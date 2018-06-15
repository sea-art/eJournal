<template>
    <div id="app">
        <header-bar/>
        <router-view class="fit-height"/>
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
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed|Roboto:400,700');

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

img {
    max-width: 100%;
    max-height: 100%;
}

.fit-height {
    flex: 1 1 auto;
    display: flex;
}

#app {
    overflow-x: hidden;
    font-family: 'Roboto', sans-serif;
    font-size: 20px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: flex;
    flex-flow: column;
    height: 100%;
    padding-top: 70px;
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
    margin-bottom: 0px;
}

h5 {
    font-size: 30px;
    margin-bottom: 0px;
}

h6 {
    font-size: 20px;
    color: var(--theme-blue);
    margin-bottom: 0px;
}

.button {
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 25px;
}

.card {
    margin-bottom: 8px;
    text-align: left;
    background-color: var(--theme-light-grey);
    border-width: 0px;
    border-left-width: 20px;
    border-radius: 0px;
}

.card-body {
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
}

.card:hover {
    background-color: var(--theme-dark-grey);
}

.card.pink-border {
    border-left-color: var(--theme-pink);
}

.card.peach-border {
    border-left-color: var(--theme-peach);
}

.card.blue-border {
    border-left-color: var(--theme-blue);
}

.portrait-container {
    height: 100px;
    width: 100px;
}
</style>
