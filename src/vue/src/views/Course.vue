<template>
    <b-row no-gutters>
        <bread-crumb :currentPage="$route.params.course"></bread-crumb>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block"></b-col>
        <b-col md="12" lg="6" order="2" class="main-content">

            <div v-for="a in assignments" :key="a.aID">
                <b-link tag="b-button" :to="{name: 'Assignment', params: {assign: a.aID}}" append>
                    <main-card :line1="a.name" :color="$route.params.color">
                        <b-progress :value="a.progress.acquired" :max="a.progress.total"/>
                    </main-card>
                </b-link>
            </div>
        </b-col>
        <b-col md="12" lg="3" order="1" order-lg="3">
            <div class="right-content">
                <h3>Upcoming</h3>
                <div v-for="d in deadlines" :key="d.dID">
                    <b-link tag="b-button" :to="{name: 'Assignment', params: {course: d.cID[0], assign: d.dID}}">
                        <todo-card :line0="d.datetime" :line1="d.name" :line2="d.course" :color="$route.params.color"></todo-card>
                    </b-link>
                </div>
            </div>
        </b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import todoCard from '@/components/TodoCard.vue'
import assignment from '@/api/assignment.js'
import getColors from '@/javascripts/colors.js'

export default {
    name: 'Course',
    data () {
        return {
            assignment: [],
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
            }],
            colors: []
        }
    },
    components: {
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'todo-card': todoCard
    },
    created () {
        assignment.get_course_assignments(this.$route.params.course)
            .then(response => { this.assignments = response })
            .catch(_ => alert('Error while loading assignments'))
            .then(_ => {this.colors = getColors(this.assignments.length)})
            .then(_ => {alert(assignment)})
    }
}
</script>
