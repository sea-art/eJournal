<template>
    <journal-student v-if="$root.canEditJournal()" :cID="cID" :aID="aID" :jID="jID"/>
    <journal-non-student v-else-if="!$root.canEditJournal() && $root.canEditJournal() != null" :cID="cID" :aID="aID" :jID="jID"/>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import journalStudent from '@/components/journal/JournalStudent.vue'
import journalNonStudent from '@/components/journal/JournalNonStudent.vue'
import breadCrumb from '@/components/BreadCrumb.vue'

export default {
    name: 'Journal',
    props: ['cID', 'aID', 'jID'],
    methods: {
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        }
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
    @import '~sass/partials/edag-page-layout.sass'
</style>
