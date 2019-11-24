<template>
    <div
        v-if="assignment.can_set_journal_name || assignment.can_set_journal_image ||
            ((assignment.can_lock_journal || !journal.locked) && assignment.is_group_assignment)"
    >
        <h3>Manage journal</h3>
        <!-- Manage every assignment -->
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
            @click="changeName()"
        >
            <icon name="save"/>
            Change name
        </b-button>
        <!-- Manage group assignment -->
        <template v-if="assignment.is_group_assignment">
            <b-button
                v-if="assignment.can_lock_journal && journal.locked"
                class="multi-form dark-bue-button full-width"
                @click="lockJournal()"
            >
                <icon name="unlock"/>
                Unlock journal
            </b-button>
            <b-button
                v-else-if="assignment.can_lock_journal"
                class="multi-form delete-button full-width"
                tag="b-button"
                @click="lockJournal()"
            >
                <icon name="lock"/>
                Lock journal
            </b-button>
            <b-button
                v-if="!journal.locked && $hasPermission('can_have_journal')"
                class="multi-form delete-button full-width"
                tag="b-button"
                @click="leaveJournal()"
            >
                <icon name="sign-out"/>
                Leave journal
            </b-button>
        </template>
    </div>
</template>
<script>
import journalAPI from '@/api/journal.js'

export default {
    name: 'ManageJournal',
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
        leaveJournal () {
            if (window.confirm('Are you sure you want to leave this journal?')) {
                journalAPI.leave(this.journal.id)
                    .then(() => {
                        this.$router.push({
                            name: 'JoinJournal',
                            params: {
                                cID: this.assignment.course.id, aID: this.assignment.id,
                            },
                        })
                    })
            }
        },
        lockJournal () {
            journalAPI.lock(this.journal.id, !this.journal.locked, { responseSuccessToast: true })
                .then(() => {
                    this.journal.locked = !this.journal.locked
                })
        },
        changeName () {
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
