<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            @edit-click="handleEdit()"
        />
        <div
            v-for="journal in journals"
            slot="main-content-column"
            :key="journal.id"
            @click="joinJournal(journal.id)"
        >
            <journal-card
                :listView="true"
                :journal="journal"
                :assignment="assignment"
            />
        </div>
    </content-columns>
</template>


<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import journalCard from '@/components/assignment/JournalCard.vue'

import journalAPI from '@/api/journal.js'
import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'JoinJournal',
    components: {
        contentColumns,
        breadCrumb,
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
