<template>
    <div id="app">
        <header-bar/>
        <router-view :key="$route.path"/>
        <feedback-section/>
    </div>
</template>

<script>
import headerBar from '@/Header.vue'
import feedbackSection from '@/FeedbackSection.vue'

export default {
    components: {
        headerBar,
        feedbackSection,
    },
}
</script>

<style lang="sass">
@import '~sass/global.sass'
@import '~sass/modules/breakpoints.sass'

#app
    overflow-x: hidden
    font-family: 'Roboto', sans-serif
    font-size: 1em
    -webkit-font-smoothing: antialiased
    -moz-osx-font-smoothing: grayscale
    padding-top: 70px
    min-height: 100%

    @include lg
        height: 100%
</style>
