<template>
    <journal-non-student v-if="!$root.canEditJournal()" :jID="this.$route.params.jID"/>
    <journal-student v-else :jID="this.$route.params.jID"/>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import journalStudent from '@/components/JournalStudent.vue'
import journalNonStudent from '@/components/JournalNonStudent.vue'
import breadCrumb from '@/components/BreadCrumb.vue'

export default {
    name: 'Journal',
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
.left-content-journal {
    flex: 0 0 auto;
}

.main-content-journal {
    padding-top: 40px !important;
    background-color: var(--theme-medium-grey);
    flex: 1 1 auto;
    overflow-x: hidden;
}

.right-content-journal {
    flex: 0 0 auto;
    padding-top: 30px !important;
    padding-left: 30px !important;
    padding-right: 30px !important;
}

@media (min-width: 1200px) {
    .outer-container {
        height: 100%;
        overflow: hidden;
    }

    .left-content-journal {
        height: 100%;
        overflow: hidden;
    }

    .main-content-journal, .right-content-journal {
        height: 100%;
        overflow-y: scroll;
    }
}

@media (max-width: 1200px) {
    .main-content-journal {
        padding-top: 0px !important;
    }
}
</style>
