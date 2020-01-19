<template>
    <div
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
            :key="`journal-member-${author.user.id}`"
            class="member"
        >
            <div
                v-if="(author.user.username == $store.getters['user/username'] && !journal.locked) ||
                    $hasPermission('can_manage_journals')"
                class="float-right"
                @click="$hasPermission('can_manage_journals') ? kickFromJournal(author.user) : leaveJournal()"
            >
                <icon
                    name="sign-out"
                    class="trash-icon"
                />
            </div>
            <b class="max-one-line">
                <b-badge
                    v-if="author.needs_lti_link"
                    v-b-tooltip.hover
                    class="background-red"
                    title="This user has not yet visited the assignment in the LMS (Canvas) yet"
                >
                    <icon
                        name="link"
                        class="fill-white"
                        scale="0.65"
                    />
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
        <div
            v-if="$hasPermission('can_manage_journals') && journal.authors.length < journal.author_limit"
            class="d-flex mt-3 flex-wrap"
        >
            <theme-select
                v-model="participantsToAdd"
                label="full_name"
                trackBy="id"
                :options="participantsWithoutJournal"
                :multiple="true"
                :searchable="true"
                :multiSelectText="`user${participantsToAdd &&
                    participantsToAdd.length === 1 ? '' : 's'} selected`"
                placeholder="Select users to add"
                class="multi-form flex-shrink-1"
            />
            <b-button
                class="add-button multi-form flex-grow-1"
                @click="addMembers">
                <icon name="user-plus"/>
                Add
            </b-button>
        </div>
    </div>
</template>

<script>
import journalAPI from '@/api/journal.js'
import assignmentAPI from '@/api/assignment.js'

import { mapGetters } from 'vuex'

export default {
    props: {
        assignment: {
            required: true,
        },
        journal: {
            required: true,
        },
    },
    data () {
        return {
            participantsToAdd: [],
            saveRequestInFlight: false,
        }
    },
    created () {
        if (this.$hasPermission('can_manage_journals')) {
            this.getParticipantsWithoutJournal()
        }
    },
    computed: {
        ...mapGetters({
            participantsWithoutJournal: 'content/assignmentParticipantsWithoutJournal',
        }),
    },
    methods: {
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
                        this.getParticipantsWithoutJournal()
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
        getParticipantsWithoutJournal () {
            assignmentAPI.getParticipantsWithoutJournal(this.assignment.id)
                .then((data) => {
                    this.$store.commit('content/SET_ASSIGNMENT_PARTICIPANTS_WITHOUT_JOURNAL', data)
                })
        },
        addMembers () {
            if (this.journal.author_limit > 1 && this.journal.authors.length + this.participantsToAdd.length >
                this.journal.author_limit) {
                this.$toasted.error('Adding these members would exceed this journal\'s member limit.')
            } else if (this.participantsToAdd.length === 0) {
                this.$toasted.error('No users selected.')
            } else {
                this.saveRequestInFlight = true
                const idsToAdd = this.participantsToAdd.reduce((acc, cur) => {
                    acc.push(cur.id)
                    return acc
                }, [])

                journalAPI.addMembers(this.journal.id, idsToAdd)
                    .then((journal) => {
                        this.journal.authors = journal.authors
                        this.saveRequestInFlight = false
                        this.getParticipantsWithoutJournal()
                        this.participantsToAdd = []
                        this.$toasted.success('Successfully added journal members.')
                    })
                    .catch(() => { this.saveRequestInFlight = false })
            }

        },
    },
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.members
    .member
        padding: 5px
        border-style: solid
        border-color: $theme-dark-grey
        border-width: 1px 0px
        .trash-icon
            margin-top: 3px
        .max-one-line
            width: calc(100% - 20px)
            .badge
                display: inline-block
                position: relative
                top: -2px
    .lock-members-icon
        float: right
        margin-top: 3px
        margin-right: 9px
        svg
            fill: red
</style>
