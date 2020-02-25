<template>
    <footer>
        <hr/>
        &copy; 2020 - eJournal (
        <a
            href="https://www.eJournal.app/changelog"
            class="text-grey"
        >
            {{ version }}</a>
        ) -
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
footer
    color: grey
    text-align: center
    width: 100%
    margin: 10px 0px
    a
        text-decoration: underline !important
</style>
