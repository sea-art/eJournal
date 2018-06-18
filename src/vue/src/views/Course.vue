<template>
    <content-columns>
        <bread-crumb slot="main-content-column" :currentPage="$route.params.courseName"></bread-crumb>
        <div slot="main-content-column" v-for="a in assignments" :key="a.aID">
            <b-link tag="b-button" :to="{ name: 'Assignment',
                                          params: {
                                              course: $route.params.course,
                                              assign: a.aID,
                                              courseName: $route.params.courseName,
                                              assignmentName: a.name
                                          }
                                        }">
                <main-card :line1="a.name" :color="$route.params.color">
                    <b-progress :value="a.progress.acquired" :max="a.progress.total"/>
                </main-card>
            </b-link>
        </div>

        <h3 slot="right-content-column">Upcoming</h3>
        <div slot="right-content-column" v-for="d in deadlines" :key="d.dID">
            <b-link tag="b-button" :to="{name: 'Assignment', params: {course: d.cID[0], assign: d.dID}}">
                <todo-card :line0="d.datetime" :line1="d.name" :line2="d.course" :color="$route.params.color"></todo-card>
            </b-link>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import todoCard from '@/components/TodoCard.vue'
import assignment from '@/api/assignment.js'
import getColors from '@/javascripts/colors.js'

export default {
    name: 'Course',
    data () {
        return {
            assignments: [],
            post: null,
            error: null
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'todo-card': todoCard
    },
    created () {
        assignment.get_course_assignments(this.$route.params.course)
            .then(response => { this.assignments = response })
            .catch(_ => alert('Error while loading assignments'))
            .then(_ => { this.colors = getColors(this.assignments.length) })
    }
}
</script>
