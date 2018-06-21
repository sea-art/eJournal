<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            @eye-click="customisePage"
            @edit-click="handleEdit()"/>

        <div slot="main-content-column" v-for="a in assignments" :key="a.aID">
            <b-link tag="b-button" :to="assignmentRoute(cID, a.aID, a.name, a.journal.jID)">
                <assignment-card :line1="a.name" :color="$root.colors[a.aID % $root.colors.length]">
                    <progress-bar v-if="a.journal && a.journal.stats" :currentPoints="a.journal.stats.acquired_points" :totalPoints="a.journal.stats.total_points"></progress-bar>
                </assignment-card>
            </b-link>
        </div>

        <main-card slot="main-content-column" class="hover" v-on:click.native="showModal('createAssignmentRef')" :line1="'+ Add assignment'"/>

        <h3 slot="right-content-column">Upcoming</h3>
        <div v-for="d in deadlines" :key="d.dID" slot="right-content-column">
            <b-link tag="b-button" :to="{name: 'Assignment', params: {cID: d.cIDs[0], aID: d.aIDs[0], dID: d.dID}}">
                <todo-card
                    :line0="d.datetime"
                    :line1="d.name"
                    :line2="d.courseAbbrs.join(', ')"
                    :color="$root.colors[d.cIDs[0] % $root.colors.length]">
                </todo-card>
            </b-link>
        </div>

        <b-modal
            slot="main-content-column"
            ref="createAssignmentRef"
            title="Create assignment"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleConfirm('createAssignmentRef')"></create-assignment>
        </b-modal>

    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import assignmentCard from '@/components/AssignmentCard.vue'
import todoCard from '@/components/TodoCard.vue'
import progressBar from '@/components/ProgressBar.vue'
import assignment from '@/api/assignment.js'
import mainCard from '@/components/MainCard.vue'
import createAssignment from '@/components/CreateAssignment.vue'

export default {
    name: 'Course',
    props: {
        cID: {
            required: true
        },
        courseName: String
    },
    data () {
        return {
            assignments: [],
            cardColor: '',
            post: null,
            error: null,
            // TODO real deadlines with API, can a deadline be bound > 1 course and assignment?
            deadlines: [{
                name: 'Individueel logboek',
                cIDs: ['1', '2'],
                aIDs: ['2', '3'],
                courseAbbrs: ['WEDA', 'PALSIE8'],
                aID: '1',
                datetime: '8-6-2018 13:00'
            }]
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'assignment-card': assignmentCard,
        'todo-card': todoCard,
        'progress-bar': progressBar,
        'main-card': mainCard,
        'create-assignment': createAssignment
    },
    created () {
        this.loadAssignments()
    },
    methods: {
        loadAssignments () {
            assignment.get_course_assignments(this.cID)
                .then(response => {
                    this.assignments = response
                })
                .catch(_ => alert('Error while loading assignments'))
        },
        showModal (ref) {
            this.$refs[ref].show()
        },
        handleConfirm (ref) {
            if (ref === 'createAssignmentRef') {
                this.loadAssignments()
            } else if (ref === 'editAssignmentRef') {
                // TODO: handle edit assignment
            }

            this.hideModal(ref)
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        customisePage () {
            alert('Wishlist: Customise page')
        },
        handleEdit () {
            this.$router.push({
                name: 'CourseEdit',
                params: {
                    cID: this.cID
                }
            })
        },
        assignmentRoute (cID, aID, name, jID) {
            if (this.$root.canViewAssignment()) {
                return {
                    name: 'Assignment',
                    params: {
                        cID: cID,
                        aID: aID,
                        assignmentName: name
                    }
                }
            } else {
                return {
                    name: 'Journal',
                    params: {
                        cID: cID,
                        aID: aID,
                        jID: jID,
                        assignmentName: name
                    }
                }
            }
        }
    }
}
</script>
