<template>
    <content-columns>
        <bread-crumb :currentPage="$route.params.course" slot="main-content-column"></bread-crumb>
        <div v-for="(a, i) in assignments" :key="a.aID" slot="main-content-column">
            <b-link tag="b-button" :to="{name: 'Assignment', params: {assign: a.aID}}" append>
                <main-card :line1="a.name" :color="$route.params.color">
                    <b-progress :value="value"/>
                </main-card>
            </b-link>
        </div>

        <h3 slot="right-content-column">Upcoming</h3>
        <!-- <div v-for="(d, i) in deadlines" :key="d.dID">
            <b-link tag="b-button" :to="{name: 'Assignment', params: {course: d.cID[0], assign: d.dID}}">
                <todo-card :line0="d.datetime" :line1="d.name" :line2="d.course" :color="colors[i]">hoi</todo-card>
            </b-link>
        </div> -->
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import assignment from '@/api/assignment.js'
import getColors from '@/javascripts/colors.js'

export default {
    name: 'Course',
    data () {
        return {
            assignments: [],
            colors: []
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'main-card': mainCard
    },
    created () {
        assignment.get_course_assignments(this.$route.params.course)
            .then(response => { this.assignments = response })
            .catch(_ => alert('Error while loading assignments'))
            .then(_ => { this.colors = getColors(this.assignments.length) })
    }
}
</script>
