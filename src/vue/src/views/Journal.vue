<template>
    <!-- TODO Permission revision should be if can_grade -->
    <journal-non-student v-if="$hasPermission('can_view_assignment_journals')" :cID="cID" :aID="aID" :jID="jID"/>
    <journal-student v-else-if="$hasPermission('can_have_journal')" :cID="cID" :aID="aID" :jID="jID"/>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import journalStudent from '@/components/journal/JournalStudent.vue'
import journalNonStudent from '@/components/journal/JournalNonStudent.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'

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
