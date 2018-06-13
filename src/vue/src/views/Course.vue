<template>
    <b-row no-gutters>
        <b-col cols="3" class="left-content"></b-col>
        <b-col cols="6" class="main-content">
            <bread-crumb :currentPage="$route.params.course"></bread-crumb>
            <b-link tag="b-button" :to="{ name: 'Assignment', params: {course: $route.params.course, assign: 1} }">
                <main-card :line1="'Colloqiumlogboek'" :line2="'4/10'"></main-card>
            </b-link>

        </b-col>
        <b-col cols="3" class="right-content"></b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import assignment from '@/api/assignment.js'

export default {
    name: 'Course',
    data () {
        return {
            assignments: []
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
    }
}
</script>
