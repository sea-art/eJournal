<template>
    <footer>
        &copy; 2020 - eJournal
        <a
            href="https://www.eJournal.app/changelog"
            class="text-grey"
        >
            {{ version }}</a>
        -
        <a
            href="mailto:support@eJournal.app"
            class="text-grey"
        >
            support@eJournal.app</a>
        -
        <a
            href="/eJournal-privacy-notice.pdf"
            class="text-grey"
        >
            Privacy notice
        </a>
    </footer>
</template>

<script>
export default {
    data () {
        return {
            version: CurrentRelease.version,
        }
    },
}

</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

footer
    border-width: 2px 2px 2px 2px
    border-color: $theme-dark-grey
    border-radius: 1em !important
    border-left: 8px solid $theme-blue
    border: 1px solid $theme-dark-grey
    color: grey
    text-align: center
    width: 100%
    margin: 10px 0px
    a
        text-decoration: underline !important
</style>
