<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            @edit-click="handleEdit()"
        />

        <div
            v-for="a in assignments"
            slot="main-content-column"
            :key="a.id"
        >
            <b-link
                :to="assignmentRoute(cID, a.id, a.journal, a.is_published)"
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
                </assignment-card>
            </b-link>
        </div>

        <b-button
            v-if="$hasPermission('can_add_assignment')"
            slot="main-content-column"
            class="add-button"
            @click="showModal('createAssignmentRef')"
        >
            <icon name="plus"/>
            Create New Assignment
        </b-button>

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
import assignmentCard from '@/components/assignment/AssignmentCard.vue'
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import deadlineDeck from '@/components/assets/DeadlineDeck.vue'

import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'Course',
    components: {
        contentColumns,
        breadCrumb,
        assignmentCard,
        createAssignment,
        deadlineDeck,
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
        }
    },
    created () {
        this.loadAssignments()
    },
    methods: {
        loadAssignments () {
            assignmentAPI.list(this.cID)
                .then((assignments) => { this.assignments = assignments })

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
        assignmentRoute (cID, aID, jID, isPublished) {
            const route = {
                params: {
                    cID,
                    aID,
                },
            }

            if (!isPublished) {
                route.name = 'FormatEdit'
            } else if (this.$hasPermission('can_view_all_journals', 'assignment', aID)) {
                route.name = 'Assignment'
            } else {
                route.name = 'Journal'
                route.params.jID = jID
            }
            return route
        },
    },
}
</script>
