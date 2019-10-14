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
            <main-card
                :line1="journal.names"
                :color="$root.getBorderClass(journal.id)"
                :line2="`${journal.students.length}/${assignment.group_size}`"
            />
        </div>
        <b-button
            slot="main-content-column"
            class="add-button"
            @click="createJournal()"
        >
            <icon name="plus"/>
            Create a new group
        </b-button>
    </content-columns>
</template>


<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import mainCard from '@/components/assets/MainCard.vue'

import journalAPI from '@/api/journal.js'
import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'CreateJoinJournal',
    components: {
        contentColumns,
        breadCrumb,
        mainCard,
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
        createJournal () {
            journalAPI.create(this.aID)
                .then((journal) => {
                    this.$router.push({
                        name: 'Journal',
                        params: {
                            cID: this.cID, aID: this.aID, jID: journal.id,
                        },
                    })
                })
            assignmentAPI.get(this.aID)
                .then((assignment) => { this.assignment = assignment })
        },
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
