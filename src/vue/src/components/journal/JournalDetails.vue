<template>
    <!-- TODO GROUPS ENGEL: Use APIs -->
    <b-card
        class="journal-details"
        :class="$root.getBorderClass($route.params.cID)"
    >
        <img
            :src="journal.image"
            class="journal-image no-hover"
        />
        <!-- TODO GROUPS ENGEL: Change permission to journal manage -->
        <span
            v-if="assignment.is_group_assignment && (assignment.can_set_journal_name || can_set_journal_image
                || $root.hasPermission('can_edit_assignment'))"
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
            <b>
                {{ journal.name }}
            </b><br/>
            <icon
                name="lock"
                class="lock-members-icon"
                :class="{
                    'fill-red': journal.locked,
                    'fill-grey': !journal.locked
                }"
            />
            <b class="member-count">
                Members ({{ journal.authors.length }}/{{ journal.author_limit }})
            </b>
            <div
                v-for="author in journal.authors.map(a => a.user)"
                :key="`journal-member-${author.username}`"
                class="member"
            >
                <icon
                    name="sign-out"
                    class="float-right trash-icon"
                />
                <b class="max-one-line">
                    {{ author.full_name }}
                </b>
                <span class="max-one-line">
                    {{ author.username }}
                </span>
            </div>
        </div>
        <b-modal
            ref="editJournalModal"
            size="lg"
            title="Edit journal"
            hideFooter
        >
            <edit-journal
                :journal="journal"
                :assignment="assignment"
            />
        </b-modal>
    </b-card>
</template>

<script>
import editJournal from '@/components/journal/EditJournal.vue'
import progressBar from '@/components/assets/ProgressBar.vue'

export default {
    components: {
        editJournal,
        progressBar,
    },
    props: {
        assignment: {
            default: null,
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
            return this.journal.name ? this.journal.name : 'Empty journal'
        },
    },
    methods: {
        showEditJournalModal () {
            this.$refs.editJournalModal.show()
        },
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
    },
}
</script>

<style lang="sass">
@import '~sass/partials/shadows.sass'
@import '~sass/modules/breakpoints.sass'
@import '~sass/modules/colors.sass'

.journal-details
    .card-body
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
