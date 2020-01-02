<template>
    <b-card
        :class="{
            'input-disabled': saveRequestInFlight,
        }"
        class="no-hover"
    >
        <div v-if="assignment.can_set_journal_image || $hasPermission('can_manage_journals')">
            <!-- TODO GROUPS: Add journal picture (croppa, like in profile picture) -->
        </div>
        <div v-if="assignment.can_set_journal_name || $hasPermission('can_manage_journals')">
            <h2 class="field-heading multi-form">
                Name
            </h2>
            <b-input
                v-model="newJournalName"
                placeholder="Journal name"
                class="theme-input multi-form"
            />
        </div>
        <div v-if="assignment.is_group_assignment && $hasPermission('can_manage_journals')">
            <h2 class="field-heading">
                Member limit
            </h2>
            <b-input
                v-model="newJournalMemberLimit"
                type="number"
                placeholder="No member limit"
                min="2"
                class="theme-input multi-form"
                required
            />
        </div>
        <b-button
            v-if="assignment.is_group_assignment && $hasPermission('can_manage_journals')"
            :class="{
                'input-disabled': !journal.members,
            }"
            :title="journal.members ? 'Cannot delete a journal with members' : 'Delete this journal'"
            v-b-tooltip.hover
            class="delete-button"
            @click="deleteJournal"
        >
            <icon name="trash"/>
            Delete journal
        </b-button>
        <b-button
            class="add-button float-right"
            @click="updateJournal"
        >
            <icon name="save"/>
            Save
        </b-button>
    </b-card>
</template>

<script>
import journalAPI from '@/api/journal.js'

export default {
    name: 'EditJournalSettings',
    props: {
        journal: {
            required: true,
        },
        assignment: {
            required: true,
        },
    },
    data () {
        return {
            newJournalName: '',
            newJournalMemberLimit: null,
            saveRequestInFlight: false,
        }
    },
    methods: {
        saveJournalSettings () {
            this.saveRequestInFlight = true
            journalAPI.update(
                this.journal.id,
                { name: this.journalName },
                { customSuccessToast: 'Successfully updated journal' })
                .then(() => {
                    this.journal.name = this.journalName
                    this.editingName = false
                    this.saveRequestInFlight = false
                })
                .catch(() => { this.saveRequestInFlight = false })
        },
        deleteJournal () {
            this.saveRequestInFlight = true
            if (window.confirm('Are you sure you want to delete this journal?')) {
                journalAPI.delete(this.journal.id, { responseSuccessToast: true })
                    .then(() => {
                        this.$emit('journal-deleted')
                        this.saveRequestInFlight = false
                    })
                    .catch(() => { this.saveRequestInFlight = false })
            }
        },
    },
}
</script>
