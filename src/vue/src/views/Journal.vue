<template>
    <journal-student v-if="$root.canEditJournal()" :cID="cID" :aID="aID" :jID="jID"/>
    <journal-non-student v-else-if="!$root.canEditJournal() && $root.canEditJournal() != null" :cID="cID" :aID="aID" :jID="jID"/>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import journalStudent from '@/components/JournalStudent.vue'
import journalNonStudent from '@/components/JournalNonStudent.vue'
import breadCrumb from '@/components/BreadCrumb.vue'

export default {
    name: 'Journal',
    props: ['cID', 'aID', 'jID'],
    data () {
        return {
            windowWidth: 0
        }
    },
    methods: {
        getWindowWidth (event) {
            this.windowWidth = document.documentElement.clientWidth
        },
        getWindowHeight (event) {
            this.windowHeight = document.documentElement.clientHeight
        },
        bootstrapLg () {
            return this.windowHeight < 1200
        },
        bootstrapMd () {
            return this.windowHeight < 922
        },
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        }
    },
    mounted () {
        this.$nextTick(function () {
            window.addEventListener('resize', this.getWindowWidth)

            this.getWindowWidth()
        })
    },
    beforeDestroy () {
        window.removeEventListener('resize', this.getWindowWidth)
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'journal-student': journalStudent,
        'journal-non-student': journalNonStudent
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.left-content-journal
    padding: 0px 30px !important
    flex: 0 0 auto

.main-content-journal
    padding-top: 40px !important
    background-color: $theme-medium-grey
    flex: 1 1 auto
    overflow-x: hidden

.right-content-journal
    flex: 0 0 auto
    padding-top: 30px !important
    padding-left: 30px !important
    padding-right: 30px !important

@media (min-width: 1200px)
    .outer-container
        height: 100%
        overflow: hidden

    .left-content-journal
        height: 100%
        overflow: hidden

    .main-content-journal, .right-content-journal
        height: 100%
        overflow-y: scroll

@media (max-width: 1200px)
    .right-content-journal
        padding: 30px !important

    .main-content-journal
        padding: 30px !important

@media (max-width: 576px)
    .left-content-journal
        padding: 0px !important

    .right-content-journal
        padding: 30px 0px !important

    .main-content-journal
        padding: 30px 0px !important
</style>
