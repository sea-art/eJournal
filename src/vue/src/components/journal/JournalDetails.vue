<template>
    <b-card
        class="journal-details"
        :class="$root.getBorderClass($route.params.cID)"
    >
        <img
            :src="journal.image"
            class="journal-image no-hover"
        />
        <span
            v-if="canManageJournal"
            class="edit-journal"
            @click="showEditJournalModal"
        >
            <icon name="edit"/>
            Edit
        </span>
        <progress-bar
            :currentPoints="journal.stats.acquired_points"
            :totalPoints="assignment.points_possible"
            :comparePoints="assignment && assignment.stats ? assignment.stats.average_points : -1"
            :bonusPoints="journal.bonus_points"
        />
        <div
            v-if="assignment.is_group_assignment"
            class="members"
        >
            <div
                @click="lockJournal"
            >
                <icon
                    v-b-tooltip.hover
                    class="lock-members-icon fill-grey"
                    :title="`Journal members are ${ journal.locked ? '' : 'not ' }locked, this journal can`
                        + `${ journal.locked ? 'not' : '' } be joined or left${ (assignment.can_lock_journal
                            || $hasPermission('can_manage_journals')) ? ': click to toggle' : ''}`"
                    :name="journal.locked ? 'lock' : 'unlock'"
                    :class="{
                        'unlocked-icon': !journal.locked && (assignment.can_lock_journal
                            || $hasPermission('can_manage_journals')),
                        'trash-icon': journal.locked && (assignment.can_lock_journal
                            || $hasPermission('can_manage_journals'))
                    }"
                />
            </div>
            <b class="member-count">
                Members
                <b
                    v-if="journal.author_limit > 1"
                    class="text-grey"
                >
                    ({{ journal.authors.length }}/{{ journal.author_limit }})
                </b>
            </b>
            <div
                v-for="author in journal.authors"
                :key="`journal-member-${author.user.username}`"
                class="member"
            >
                <div
                    v-if="(author.user.username == $store.getters['user/username'] && !journal.locked) ||
                        $hasPermission('can_manage_journals')"
                    @click="$hasPermission('can_manage_journals') ? kickFromJournal(author.user) : leaveJournal()"
                >
                    <icon
                        name="sign-out"
                        class="float-right trash-icon"
                    />
                </div>
                <b class="max-one-line">
                    <b-badge
                        v-if="author.needs_lti_link"
                        v-b-tooltip.hover
                        class="red float-right"
                        title="Not linked via LTI"
                    >
                        <icon name="unlink"/>
                    </b-badge>
                    {{ author.user.full_name }}
                </b>
                <span class="max-one-line">
                    {{ author.user.username }}
                </span>
            </div>
            <div
                v-if="journal.authors.length === 0"
                class="member text-grey"
            >
                No members yet
            </div>
        </div>
        <b-modal
            v-if="canManageJournal"
            ref="editJournalSettingsModal"
            size="lg"
            title="Edit journal"
            hideFooter
        >
            <edit-journal-settings
                :journal="journal"
                :assignment="assignment"
                @journal-updated="hideEditJournalModal"
                @journal-deleted="$router.push(assignmentRoute(assignment))"
            />
        </b-modal>
    </b-card>
</template>

<script>
import editJournalSettings from '@/components/journal/EditJournalSettings.vue'
import progressBar from '@/components/assets/ProgressBar.vue'
import journalAPI from '@/api/journal.js'

export default {
    components: {
        editJournalSettings,
        progressBar,
    },
    props: {
        assignment: {
            required: true,
        },
        journal: {
            required: true,
        },
        listView: {
            default: false,
        },
        editView: {
            default: false,
        },
    },
    computed: {
        journalAuthorUsername () {
            if (this.journal.authors && this.journal.authors.length > 0) {
                return this.journal.authors[0].user.username
            }
            return ''
        },
        journalName () {
            return this.journal.name
        },
        canManageJournal () {
            return this.assignment.is_group_assignment && (this.assignment.can_set_journal_name
                || this.assignment.can_set_journal_image || this.$hasPermission('can_grade'))
        },
    },
    methods: {
        showEditJournalModal () {
            this.$refs.editJournalSettingsModal.show()
        },
        hideEditJournalModal () {
            this.$refs.editJournalSettingsModal.hide()
        },
        leaveJournal () {
            if (window.confirm('Are you sure you want to leave this journal?'
                + `${this.journal.authors.length === 1 ? ' Since you are the last member of this journal, doing so '
                + 'will reset the journal and remove all its entries. This action cannot be undone.' : ''}`)) {
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
        kickFromJournal (user) {
            if (window.confirm(`Are you sure you want to remove ${user.full_name} from this journal?`
                + `${this.journal.authors.length === 1 ? ' Since they are the last member of this journal, doing so '
                + 'will reset the journal and remove all its entries. This action cannot be undone.' : ''}`)) {
                journalAPI.kick(this.journal.id, user.id, { responseSuccessToast: true })
                    .then(() => {
                        this.journal.authors = this.journal.authors.filter(author => author.user.id !== user.id)
                        if (this.journal.authors.length === 0) {
                            this.$router.push(this.assignmentRoute(this.assignment))
                        }
                    })
            }
        },
        lockJournal () {
            if (this.assignment.can_lock_journal || this.$hasPermission('can_manage_journals')) {
                journalAPI.lock(this.journal.id, !this.journal.locked, { responseSuccessToast: true })
                    .then(() => {
                        this.journal.locked = !this.journal.locked
                    })
            }
        },
        assignmentRoute (assignment) {
            const route = {
                params: {
                    cID: assignment.course.id,
                    aID: assignment.id,
                },
            }

            if (this.$hasPermission('can_view_all_journals', 'assignment', assignment.id)) {
                if (!assignment.is_published) { // Teacher not published route
                    route.name = 'FormatEdit'
                } else { // Teacher published route
                    route.name = 'Assignment'
                }
            } else if (assignment.is_group_assignment && assignment.journal === null) {
                // Student new group assignment route
                route.name = 'JoinJournal'
            } else { // Student with journal route
                route.name = 'Journal'
                route.params.jID = assignment.journal
            }

            return route
        },
    },
}
</script>

<style lang="sass">
@import '~sass/partials/shadows.sass'
@import '~sass/modules/breakpoints.sass'
@import '~sass/modules/colors.sass'

.journal-details
    &>.card-body
        padding-top: 45px
    .journal-image
        @extend .shadow
        position: absolute
        width: 70px
        height: 70px
        left: 50%
        top: -25px
        margin-left: -35px
        border-radius: 50% !important
        background-color: white
    .edit-journal
        position: absolute
        right: 10px
        top: 5px
        color: grey
        svg
            margin-top: -2px
            fill: grey !important
        &:hover:not(.no-hover)
            cursor: pointer
            color: darken(grey, 20)
            svg
                fill: darken(grey, 20) !important
    .members
        margin-top: 10px
        .member
            padding: 5px
            border-style: solid
            border-color: $theme-dark-grey
            border-width: 1px 0px
            .trash-icon
                margin-top: 3px
            .max-one-line
                width: calc(100% - 20px)
        .lock-members-icon
            float: right
            margin-top: 3px
            margin-right: 9px
            svg
                fill: red
</style>
