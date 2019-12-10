<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            @edit-click="handleEdit()"
        />
        <journal-card
            v-for="journal in journals"
            slot="main-content-column"
            :key="`join-journal-${journal.id}`"
            :listView="true"
            :journal="journal"
            :assignment="assignment"
            :class="{ 'input-disabled': journal.authors.length >= journal.author_limit }"
            @click.native="joinJournal(journal.id)"
        />
        <main-card
            v-if="journals.length === 0"
            slot="main-content-column"
            line1="No journals for this assignment"
            line2="Please ask your teacher to create a journal for you to join."
            class="no-hover border-dark-grey"
        />
    </content-columns>
</template>


<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import mainCard from '@/components/assets/MainCard.vue'
import journalCard from '@/components/assignment/JournalCard.vue'

import journalAPI from '@/api/journal.js'
import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'JoinJournal',
    components: {
        contentColumns,
        breadCrumb,
        mainCard,
        journalCard,
    },
    props: {
        cID: {
            required: true,
        },
        aID: {
            required: true,
        },
    },
    data () {
        return {
            journals: [],
            assignment: null,
            loadingJournals: true,
        }
    },
    created () {
        const initialCalls = []
        initialCalls.push(assignmentAPI.get(this.aID, this.cID))
        initialCalls.push(journalAPI.list(this.cID, this.aID))
        Promise.all(initialCalls).then((results) => {
            this.loadingJournals = false
            this.assignment = results[0]
            this.journals = results[1]
        })
    },
    methods: {
        joinJournal (jID) {
            journalAPI.join(jID)
                .then((journal) => {
                    this.$router.push({
                        name: 'Journal',
                        params: {
                            cID: this.cID, aID: this.aID, jID: journal.id,
                        },
                    })
                })
        },
    },
}
</script>
