<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            @edit-click="handleEdit()"
        />

        <load-wrapper
            slot="main-content-column"
            :loading="loadingAssignments"
        >
            <div
                v-for="a in assignments"
                :key="a.id"
            >
                <b-link
                    :to="assignmentRoute(a)"
                    tag="b-button"
                >
                    <assignment-card
                        :assignment="a"
                        :uniqueName="!assignments.some(a2 =>
                            a.name === a2.name && a.id !== a2.id
                        )"
                    >
                        <b-button
                            v-if="$hasPermission('can_edit_assignment', 'assignment', a.id)"
                            class="change-button float-right"
                            @click.prevent.stop="editAssignment(a)"
                        >
                            <icon name="edit"/>
                            Edit
                        </b-button>
                        <b-button
                            v-else-if="$hasPermission('can_have_journal', 'assignment', a.id) && a.is_group_assignment"
                            class="float-right"
                            @click.prevent.stop="$router.push({
                                name: 'JoinJournal',
                                params: {
                                    cID: cID,
                                    aID: a.id,
                                    viewing: true,
                                },
                            })"
                        >
                            <icon name="users"/>
                            View journals
                        </b-button>
                    </assignment-card>
                </b-link>
            </div>
            <main-card
                v-if="assignments !== null && assignments.length === 0"
                line1="No assignments found"
                line2="This course currently does not have any assignments."
                class="no-hover border-dark-grey"
            />
            <b-button
                v-if="$hasPermission('can_add_assignment', 'course', cID)"
                class="add-button mr-2 mb-2"
                @click="showModal('createAssignmentRef')"
            >
                <icon name="plus"/>
                Create new assignment
            </b-button>
            <b-button
                v-if="$hasPermission('can_add_assignment', 'course', cID)"
                v-b-modal="'course-assignment-copy-modal'"
                class="add-button mb-2"
            >
                <icon name="file"/>
                Copy Assignment
            </b-button>
            <assignment-copy-modal
                modalID="course-assignment-copy-modal"
                :cID="cID"
            />
        </load-wrapper>

        <b-modal
            slot="main-content-column"
            ref="createAssignmentRef"
            title="Create new assignment"
            size="lg"
            hideFooter
        >
            <create-assignment @handleAction="handleCreated"/>
        </b-modal>

        <deadline-deck slot="right-content-column"/>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import loadWrapper from '@/components/loading/LoadWrapper.vue'
import assignmentCard from '@/components/assignment/AssignmentCard.vue'
import mainCard from '@/components/assets/MainCard.vue'
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import deadlineDeck from '@/components/assets/DeadlineDeck.vue'
import assignmentCopyModal from '@/components/assignment/AssignmentCopyModal.vue'

import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'Course',
    components: {
        contentColumns,
        breadCrumb,
        loadWrapper,
        assignmentCard,
        mainCard,
        createAssignment,
        deadlineDeck,
        assignmentCopyModal,
    },
    props: {
        cID: {
            required: true,
        },
    },
    data () {
        return {
            assignments: null,
            cardColor: '',
            post: null,
            error: null,
            deadlines: [],
            loadingAssignments: true,
        }
    },
    created () {
        this.loadAssignments()
    },
    methods: {
        loadAssignments () {
            assignmentAPI.list(this.cID)
                .then((assignments) => {
                    this.assignments = assignments
                    this.loadingAssignments = false
                })

            assignmentAPI.getUpcoming(this.cID)
                .then((deadlines) => { this.deadlines = deadlines })
        },
        handleEdit () {
            this.$router.push({
                name: 'CourseEdit',
                params: {
                    cID: this.cID,
                },
            })
        },
        editAssignment (assignment) {
            this.$router.push({
                name: 'FormatEdit',
                params: {
                    cID: this.cID,
                    aID: assignment.id,
                },
            })
        },
        handleCreated (aID) {
            this.$router.push({
                name: 'FormatEdit',
                params: {
                    cID: this.cID,
                    aID,
                },
            })
        },
        showModal (ref) {
            this.$refs[ref].show()
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
