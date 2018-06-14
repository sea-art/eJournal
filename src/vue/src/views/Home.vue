<template>
    <content-columns>
        <bread-crumb slot="main-content-column" :currentPage="'Courses'"></bread-crumb>
        <div v-for="(c, i) in courses" :key="c.cID" slot="main-content-column">
            <b-link tag="b-button" :to="{name: 'Course', params: {course: c.cID, courseName: c.name, color: colors[i]}}">
                <main-card :line1="c.name" :line2="c.date" :color="colors[i]">hoi</main-card>
            </b-link>
        </div>

        <h3 slot="right-content-column">Upcoming</h3>
        <div v-for="(d, i) in deadlines" :key="d.dID" slot="right-content-column">
            <b-link tag="b-button" :to="{name: 'Assignment', params: {course: d.cID[0], assign: d.dID}}">
                <todo-card :line0="d.datetime" :line1="d.name" :line2="d.course" :color="colors[i]">hoi</todo-card>
            </b-link>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import todoCard from '@/components/TodoCard.vue'
import course from '@/api/course'
import getColors from '@/javascripts/colors.js'
/* import assignment from '@/api/assignment' */

export default {
    name: 'Home',
    data () {
        return {
            colors: [],
            courses: [],
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
        'main-card': mainCard,
        'todo-card': todoCard
    },
    created () {
        course.get_user_courses()
            .then(response => { this.courses = response })
            .catch(_ => alert('Error while loading courses'))
            .then(_ => { this.colors = getColors(this.courses.length) })

        /* assignment.get_upcoming_deadlines()
           .then(response => { this.deadlines = response })
           .catch(_ => alert('Error while loading deadlines')) */
    }
}
</script>
