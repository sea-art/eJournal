<template>
    <div v-if="computedDeadlines.length > 0">
        <h3 slot="right-content-column">
            To Do
        </h3>
        <!-- TODO: This seems like an inappropriate permission check. Will have to be reconsidered in the rework. -->
        <b-form-select
            v-if="showSortBy && computedDeadlines.length > 1"
            v-model="selectedSortOption"
            :selectSize="1"
            class="multi-form"
        >
            <option value="date">
                Sort by date
            </option>
            <option value="markingNeeded">
                Sort by marking needed
            </option>
        </b-form-select>

        <div
            v-for="(d, i) in computedDeadlines"
            :key="i"
        >
            <b-link
                :to="assignmentRoute(d)"
                tag="b-button"
            >
                <todo-card
                    :deadline="d"
                    :course="d.course"
                />
            </b-link>
        </div>
    </div>
</template>

<script>
import assignmentAPI from '@/api/assignment.js'

import todoCard from '@/components/assets/TodoCard.vue'
import { mapGetters, mapMutations } from 'vuex'

export default {
    components: {
        todoCard,
    },
    data () {
        return {
            deadlines: [],
        }
    },
    computed: {
        ...mapGetters({
            sortBy: 'preferences/todoSortBy',
        }),
        selectedSortOption: {
            get () {
                return this.sortBy
            },
            set (value) {
                this.setSortBy(value)
            },
        },
        computedDeadlines () {
            function compareDate (a, b) {
                if (!a.deadline.date) { return 1 }
                if (!b.deadline.date) { return -1 }
                return new Date(a.deadline.date) - new Date(b.deadline.date)
            }

            function compareMarkingNeeded (a, b) {
                return (b.stats.needs_marking + b.stats.unpublished) - (a.stats.needs_marking + a.stats.unpublished)
            }

            let deadlines = this.deadlines
            if (this.$hasPermission('can_add_course')) {
                deadlines = deadlines.filter(
                    d => d.stats.needs_marking + d.stats.unpublished > 0 || !d.is_published)
            } else {
                deadlines = deadlines.filter(
                    d => d.deadline.date !== null)
            }

            if (this.selectedSortOption === 'date') {
                deadlines.sort(compareDate)
            } else if (this.selectedSortOption === 'markingNeeded') {
                deadlines.sort(compareMarkingNeeded)
            }

            return deadlines
        },
        showSortBy () {
            return Object.entries(this.$store.getters['user/permissions']).some(
                ([key, value]) => ((key.indexOf('assignment') >= 0) && value.can_grade))
        },
    },
    created () {
        assignmentAPI.getUpcoming(this.$route.params.cID)
            .then((deadlines) => { this.deadlines = deadlines })
    },
    methods: {
        ...mapMutations({
            setSortBy: 'preferences/SET_TODO_SORT_BY',
        }),
        assignmentRoute (assignment) {
            const route = {
                params: {
                    cID: assignment.course.id,
                    aID: assignment.id,
                },
            }

            if (!assignment.isPublished) { // Teacher not published route
                route.name = 'FormatEdit'
            } else if (this.$hasPermission('can_view_all_journals', 'assignment', assignment.id)) {
                // Teacher published route
                route.name = 'Assignment'
            } else if (assignment.journal === null && assignment.is_group_assignment) {
                // Student new group assignment route
                route.name = 'JoinJournal'
            } else { // Student with journal route
                route.name = 'Journal'
                route.params.jID = assignment.journal
            }
            return route
        },
    },
}
</script>
