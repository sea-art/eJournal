<template>
    <content-columns>
        <bread-crumb slot="main-content-column" :currentPage="'Assignments'"></bread-crumb>
        <div slot="main-content-column" v-for="a in assignments" :key="a.aID">
            {{a}}
            <b-link tag="b-button" :to="{ name: 'Journal',
                                          params: {
                                              course: a.course,
                                              assign: a.aID,
                                              student: 'Rick',
                                              color: 'pink-border',
                                              courseName: a.courseName,
                                              assignmentName: a.assignmentName,
                                              journalName: 'brick'
                                          }
                                        }">
                <main-card :line1="a.courseName">
                    <b-progress :value="a.progress.acquired" :max="a.progress.total"/>
                </main-card>
            </b-link>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import studentCard from '@/components/StudentCard.vue'
import mainCard from '@/components/MainCard.vue'
// import assignments from '@/api/assignmentsOverview.js'

export default {
    name: 'AssignmentsOverview',
    data () {
        return {
            assignments: [{
                course: '1',
                assign: '1',
                courseName: 'Portfolio Academische Vaardigheden 2',
                assignmentName: 'Logboek',
                progress: {'acquired': 5, 'total': 10}
            },
            {
                course: '1',
                assign: '3',
                courseName: 'Beeldbewerken',
                assignmentName: 'Logboek',
                progress: {'acquired': 2, 'total': 10}
            }]
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'student-card': studentCard
    }
}
</script>
