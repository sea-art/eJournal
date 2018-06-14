<template>
    <b-row no-gutters>
        <b-col cols="3" class="left-content"></b-col>
        <b-col cols="6" class="main-content">
            <bread-crumb :currentPage="$route.params.course"></bread-crumb>
            <div v-for="(a, i) in assignments" :key="a.aID">
                <b-link tag="b-button" :to="{name: 'Assignment', params: {assign: a.aID}}" append>
                    <main-card :line1="a.name" :color="$route.params.color">
                        <b-progress :value="value"/>
                    </main-card>
                </b-link>
            </div>
        </b-col>
        <b-col cols="3" class="right-content"></b-col>
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
