<!--TODO Check teacher permission;
    TODO Display student cards of those enrolled
    TODO Add deck of work to be checked for this assignment -->

<template>
    <content-columns>
        <bread-crumb @eye-click="customisePage" :currentPage="Placeholder" :course="Placeholder" slot="main-content-column"></bread-crumb>
        <div v-for="journal in assignmentJournals" :key="journal.student.uID" slot="main-content-column">
            <b-link tag="b-button" :to="{ name: 'Journal',
                                          params: {
                                              cID: cID,
                                              aID: aID,
                                              jID: journal.student.uID
                                          }
                                        }">
                <student-card
                    :student="j.student.name"
                    :studentNumber="j.student.uID"
                    :portraitPath="j.student.picture"
                    :progress="j.progress"
                    :stats="j.stats"
                    :color="$root.colors[j.uid % $root.colors.length]">
                </student-card>
            </b-link>
        </div>
        <div slot="right-content-column">
            <h3>Statistics</h3>
            <statistics-card :color="cardColor" :subject="'Needs marking'" :num="stats.needsMarking"></statistics-card>
            <statistics-card :color="cardColor" :subject="'Average points'" :num="stats.avgPoints"></statistics-card>
            <statistics-card :color="cardColor" :subject="'Median points'" :num="stats.medianPoints"></statistics-card>
            <statistics-card :color="cardColor" :subject="'Average entries'" :num="stats.avgEntries"></statistics-card>
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
    props: {
        cID: {
            type: Number,
            required: true
        },
        aID: {
            type: Number,
            required: true
        },
        assignmentName: ''
    },
    data () {
        return {
            assignJournals: [],
            stats: [],
            cardColor: ''
        }
    },
    components: {
        'content-columns': contentColumns,
        'student-card': studentCard,
        'statistics-card': statisticsCard,
        'bread-crumb': breadCrumb
    },
    created () {
        journal.get_assignment_journals(this.aID)
            .then(response => {
                this.assignmentJournals = response.journals
                this.stats = response.stats
            })
            .catch(_ => alert('Error while loading jounals'))
    },
    methods: {
        customisePage () {
            alert('Wishlist: Customise page')
        }
    }
}
</script>
