<template>
    <footer>
        <hr/>
        &copy; 2019 - eJournal.app -
        <a
            href="/eJournal-privacy-notice.pdf"
            class="text-grey"
        >
            Privacy notice
        </a>
        <tooltip
            tip="We reserve the right to change this privacy policy as we may deem necessary from time to time or as
            may be required by law. Any changes will be immediately posted on the website and you are deemed to have
            accepted the terms of the privacy policy on your first use of the website following the alterations."
        />
    </footer>
</template>
<script>
import tooltip from '@/components/assets/Tooltip.vue'

export default {
    components: {
        tooltip,
    },
}

</script>

<style lang="sass">
footer
    color: grey
    text-align: center
    width: 100%
    margin: 10px 0px
</style>
