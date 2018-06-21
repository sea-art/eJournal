<template>
    <journal-student :cID="cID" :aID="aID" :jID="jID"/>
    <!-- <journal-non-student :cID="cID" :aID="aID" :jID="jID"/> -->
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
            alert('Wishlist: Customise page')
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

<style>
.noHoverCard:hover {
    background-color: var(--theme-light-grey);
}
</style>
