<!--TODO Check teacher permission;
    TODO Display student cards of those enrolled
    TODO Add deck of work to be checked for this assignment -->

<template>
    <b-row no-gutters>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block"></b-col>
        <b-col md="12" lg="6" order="2" class="main-content">
            <h1>Assignment Page</h1>
            <div v-for="journal in assignmentJournals" :key="journal.uid">
                <b-link tag="b-button" :to="{ name: 'Journal', params: {course: journal.uid} }">
                    <student-card
                        :student="journal.student"
                        :studentNumber="journal.studentNumber"
                        :studentPortraitPath="journal.studentPortraitPath"
                        :progress="journal.progress"
                        :entriesStats="journal.entriesStats">
                    </student-card>
                </b-link>
            </div>
        </b-col>
        <b-col md="12" lg="3" order="1" order-lg="3" class="right-content">Notifications</b-col>
    </b-row>
</template>

<script>
import studentCard from '@/components/StudentCard.vue'

export default {
    name: 'Assignment',
    data () {
        return {
            assignmentJournals: [{
                student: 'Maarten van Keulen',
                studentNumber: '6066364',
                studentPortraitPath: '../assets/logo.png',
                progress: {acquired: 10, total: 10},
                entriesStats: {graded: 1, total: 1},
                uid: 1
            }, {
                student: 'Dennis Wind',
                studentNumber: '1111111',
                studentPortraitPath: '../assets/logo.png',
                progress: {acquired: 8, total: 10},
                entriesStats: {graded: 1, total: 1},
                uid: 2
            }]
        }
    },
    components: {
        'student-card': studentCard
    }
}
</script>
