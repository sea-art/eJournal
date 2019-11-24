<template>
    <content-columns>
        <bread-crumb slot="main-content-column"/>
        <div slot="main-content-column">
            <journal-card
                v-for="journal in journals"
                :key="journal.id"
                :journal="journal"
                :editView="true"
                :assignment="assignment"
            />
        </div>
        <div slot="right-content-column">
            <h3>Actions</h3>
            <b-button
                v-if="$hasPermission('can_edit_assignment')"
                class="multi-form change-button full-width"
                @click.prevent.stop="$router.push({ name: 'FormatEdit', params: { cID: cID, aID: aID } })"
            >
                <icon name="edit"/>
                Edit format
            </b-button>
        </div>
    </content-columns>
</template>

<script>
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import contentColumns from '@/components/columns/ContentColumns.vue'
import journalCard from '@/components/assignment/JournalCard.vue'

import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'JournalsEdit',
    components: {
        breadCrumb,
        contentColumns,
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
            assigment: {},
            journals: [],
        }
    },
    computed: {

    },
    created () {
        assignmentAPI.get(this.aID, this.cID)
            .then((assignment) => {
                this.assignment = assignment
                this.journals = assignment.journals
            })
        // journalAPI.list(this.cID, this.aID)
        //     .then((journals) => {
        //         this.journals = journals
        //     })
    },
}
</script>
