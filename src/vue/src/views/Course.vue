<template>
    <b-row no-gutters>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block"></b-col>
        <b-col md="12" lg="6" order="2" class="main-content">
            <bread-crumb :currentPage="$route.params.course"></bread-crumb>

            <div v-for="(a, i) in assignments" :key="a.aID">
                <b-link tag="b-button" :to="{name: 'Assignment', params: {assign: a.aID}}" append>
                    <main-card :line1="a.name" :color="$route.params.color">
                        <b-progress :value="value"/>
                    </main-card>
                </b-link>
            </div>
        </b-col>
        <b-col md="12" lg="3" order="1" order-lg="3">
            <div class="right-content">
                <h3>Upcoming</h3>
                <!-- <div v-for="(d, i) in deadlines" :key="d.dID">
                    <b-link tag="b-button" :to="{name: 'Assignment', params: {course: d.cID[0], assign: d.dID}}">
                        <todo-card :line0="d.datetime" :line1="d.name" :line2="d.course" :color="colors[i]">hoi</todo-card>
                    </b-link>
                </div> -->
            </div>
        </b-col>
    </b-row>
</template>

<script>
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
        'bread-crumb': breadCrumb,
        'main-card': mainCard
    },
    created () {
        assignment.get_course_assignments(this.$route.params.course)
            .then(response => { this.assignments = response })
            .catch(_ => alert('Error while loading assignments'))
            .then(_ => {this.colors = getColors(this.assignments.length)})
    }
}
</script>
