<template>
    <content-columns>
        <div slot="main-content-column">
            <b-button class="float-right edit-button" :to="{ name: 'AssignmentEdit',
                                                             params: { cID: cID,
                                                                       aID: aID}}">
                Edit
            </b-button>
        </div>
        <bread-crumb slot="main-content-column" @eye-click="customisePage"/>
        <div v-if="assignmentJournals.length > 0" v-for="journal in assignmentJournals" :key="journal.student.uID" slot="main-content-column">
            <b-link tag="b-button" :to="{ name: 'Journal',
                                          params: {
                                              cID: cID,
                                              aID: aID,
                                              jID: journal.jID
                                          }
                                        }">
                <student-card
                    :student="journal.student.name"
                    :studentNumber="journal.student.uID"
                    :portraitPath="journal.student.picture"
                    :stats="journal.stats"
                    :color="$root.colors[journal.uid % $root.colors.length]">
                </student-card>
            </b-link>
        </div>
        <div v-if="assignmentJournals.length === 0" slot="main-content-column">
            <h1>No journals found</h1>
        </div>
        <div  v-if="stats" slot="right-content-column">
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
            required: true
        },
        aID: {
            required: true
        },
        assignmentName: ''
    },
    data () {
        return {
            assignmentJournals: [],
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
