<template>
    <content-columns>
        <bread-crumb @eye-click="customisePage" slot="main-content-column" :currentPage="courseName">
        </bread-crumb>
        <div slot="main-content-column" v-for="a in assignments" :key="a.aID">
            <b-link tag="b-button" :to="{ name: 'Assignment',
                                          params: {
                                              cID: cID,
                                              aID: a.aID,
                                              assignmentName: a.name
                                          }
                                        }">
                <assignment-card :line1="a.name" :color="$root.colors[a.aID % $root.colors.length]">
                    <progress-bar :currentPoints="a.progress.acquired" :totalPoints="a.progress.total"></progress-bar>
                </assignment-card>
            </b-link>
        </div>

        <h3 slot="right-content-column">Upcoming</h3>
        <!-- <div slot="right-content-column" v-for="d in deadlines" :key="d.dID">
            <b-link tag="b-button" :to="{name: 'Assignment', params: {course: d.cID[0], assign: d.dID}}">
                <todo-card :line0="d.datetime" :line1="d.name" :line2="d.course" :color="cardColor"></todo-card>
            </b-link>
        </div> -->
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import assignmentCard from '@/components/AssignmentCard.vue'
import todoCard from '@/components/TodoCard.vue'
import progressBar from '@/components/ProgressBar.vue'
import assignment from '@/api/assignment.js'

export default {
    name: 'Course',
    props: {
        cID: {
            type: String,
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
            deadlines: [{
                name: 'Individueel logboek',
                course: 'WEDA',
                cID: ['2017WDB'],
                dID: '2017IL1',
                datetime: '8-6-2018 13:00'
            }, {
                name: 'Logboek academia',
                course: 'AVI2',
                cID: ['2017AVI2'],
                dID: '2017LA',
                datetime: '8-6-2018 13:00'
            }, {
                name: 'Individueel logboek',
                course: 'AVI1, AVI2',
                cID: ['2017AVI1', '2017AVI2'],
                dID: '2017IL2',
                datetime: '8-6-2018 13:00'
            }]
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'assignment-card': assignmentCard,
        'todo-card': todoCard,
        'progress-bar': progressBar
    },
<<<<<<< HEAD
    created () {
        assignment.get_course_assignments(this.$route.params.course)
            .then(response => { this.assignments = response })
            .catch(_ => alert('Error while loading assignments'))
            .then(_ => { this.colors = getColors(this.assignments.length) })

    },
=======
>>>>>>> 31ad5c47753ddd3671534a282a0faf0d81a2899a
    methods: {
        customisePage () {
            alert('Wishlist: Customise page')
        }
    },
    created () {
        assignment.get_course_assignments(this.cID)
            .then(response => { this.assignments = response })
            .catch(_ => alert('Error while loading assignments'))
    }
}
</script>
