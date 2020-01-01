<template>
    <b-card class="no-hover">
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
        <div v-if="$hasPermission('can_manage_journals')">
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
        <b-button class="add-button float-right">
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
            newJournalMemberLimit: 0,
        }
    },
    methods: {
        saveJournalSettings () {
            journalAPI.update(
                this.journal.id,
                { name: this.journalName },
                { customSuccessToast: 'Successfully updated journal' })
                .then(() => {
                    this.journal.name = this.journalName
                    this.editingName = false
                })
        },
        deleteJournal () {
            if (window.confirm('Are you sure you want to delete this journal?')) {
                journalAPI.delete(this.journal.id, { responseSuccessToast: true })
            }
        },
    },
}
</script>
