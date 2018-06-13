<template>
    <b-row no-gutters>
        <b-col cols="3" class="left-content"></b-col>
        <b-col cols="6" class="main-content">
            <bread-crumb :currentPage="$route.params.course"></bread-crumb>

            <b-link tag="b-button" :to="{ name: 'Assignment', params: {course: $route.params.course, assign: assignments[0].name} }">
                <main-card :line1="'Colloqiumlogboek'" :line2="'4/10'"></main-card>
            </b-link>

        </b-col>
        <b-col cols="3" class="right-content"></b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'

export default {
    name: 'Course',
    data () {
        return {
            assignments: [{
                name: 'Colloqiumlogboek',
                auth: 'Robert van Wijk',
                progress: '4/10'
            }]
        }
    },
    components: {
        'bread-crumb': breadCrumb,
        'main-card': mainCard
    }
}
</script>
