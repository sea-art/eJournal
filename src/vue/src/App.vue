<template>
    <div id="app">
        <header-bar/>
        <router-view :key="$route.path" class="fit-height"/>
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

<style lang="sass">
@import '~sass/global.sass'

#app
    overflow-x: hidden
    font-family: 'Roboto', sans-serif
    font-size: 1em
    -webkit-font-smoothing: antialiased
    -moz-osx-font-smoothing: grayscale
    display: flex
    flex-flow: column
    height: 100%
    padding-top: 70px
</style>
