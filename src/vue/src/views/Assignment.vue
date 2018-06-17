<!--TODO Check teacher permission;
    TODO Display student cards of those enrolled
    TODO Add deck of work to be checked for this assignment -->

<template>
    <content-columns>
        <bread-crumb :currentPage="$route.params.assignmentName" :course="$route.params.courseName" slot="main-content-column"></bread-crumb>
        <div v-for="j in assignJournals" :key="j.uid" slot="main-content-column">
            <b-link tag="b-button" :to="{ name: 'Journal',
                                          params: {
                                              course: $route.params.course,
                                              assign: $route.params.assign,
                                              student: 'Rick',
                                              color: $route.params.color,
                                              courseName: $route.params.courseName,
                                              assignmentName: $route.params.assignmentName,
                                              journalName: j.student
                                          }
                                        }">
                <student-card
                    :student="j.student"
                    :studentNumber="j.studentnumber"
                    :studentPortraitPath="j.studentPortraitPath"
                    :studentProgress="j.progress"
                    :entryStats="j.entryStats">
                </student-card>
            </b-link>
        </div>
        <div slot="right-content-column">
            <h3>Statistics</h3>
            <statistics-card :subject="'Needs marking'" :num="stats.needsMarking"></statistics-card>
            <statistics-card :subject="'Average points'" :num="stats.avgPoints"></statistics-card>
            <statistics-card :subject="'Median points'" :num="stats.medianPoints"></statistics-card>
            <statistics-card :subject="'Average entries'" :num="stats.avgEntries"></statistics-card>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import studentCard from '@/components/StudentCard.vue'
import statisticsCard from '@/components/StatisticsCard.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import journal from '@/api/journal.js'

export default {
    name: 'Assignment',
    data () {
        return {
            assignJournals: [],
            stats: []
        }
    },
    components: {
        'content-columns': contentColumns,
        'student-card': studentCard,
        'statistics-card': statisticsCard,
        'bread-crumb': breadCrumb
    },
    created () {
        journal.get_assignment_journals(this.$route.params.assign)
            .then(response => {
                this.assignJournals = response.journals
                this.stats = response.stats
            }).catch(_ => alert('Error while loading jounals'))
    }
}
</script>
