<template>
    <footer>
        <hr/>
        &copy; 2020 - eJournal (
        <a
            href="https://www.eJournal.app/changelog"
            class="text-grey underline"
        >
            {{ version }}
        </a>
        ) -
        <a
            href="/eJournal-privacy-notice.pdf"
            class="text-grey underline"
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
    a.underline
        text-decoration: underline !important
</style>
