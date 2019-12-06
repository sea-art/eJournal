<template>
    <b-card
        v-if="assignment.can_set_journal_name || assignment.can_set_journal_image ||
            ((assignment.can_lock_journal || (!journal.locked && $hasPermission('can_have_journal'))) &&
            assignment.is_group_assignment)"
    >
        <input
            v-if="assignment.can_set_journal_name && editingName"
            v-model="journalName"
            class="theme-input full-width multi-form"
            type="text"
            :placeholder="journal.name"
        />
        <b-button
            v-if="assignment.can_set_journal_name"
            class="multi-form change-button full-width"
            @click="editName()"
        >
            <icon name="save"/>
            Change name
        </b-button>
    </b-card>
</template>
<script>
import journalAPI from '@/api/journal.js'

export default {
    name: 'EditJournal',
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
            editingName: false,
            journalName: '',
        }
    },
    methods: {
        editName () {
            if (this.editingName && this.journalName) {
                journalAPI.update(
                    this.journal.id,
                    { name: this.journalName },
                    { customSuccessToast: 'Successfully set journal name' })
                    .then(() => {
                        this.journal.name = this.journalName
                        this.editingName = false
                    })
            } else {
                this.editingName = true
            }
        },
    },
}
</script>
