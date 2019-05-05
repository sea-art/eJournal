<template>
    <div>
        <!-- TODO: This seems like an inappropriate permission check. Will have to be reconsidered in the rework. -->
        <b-form-select
            v-if="$hasPermission('can_add_course')"
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
                v-if="d.course"
                :to="assignmentRoute(d.course.id, d.id, d.journal, d.is_published)"
                tag="b-button"
            >
                <todo-card
                    :deadline="d"
                    :course="d.course"
                />
            </b-link>
            <b-link
                v-for="(course, j) in d.courses"
                v-else
                :key="`${i}-${j}`"
                :to="assignmentRoute(course.id, d.id, d.journal, d.is_published)"
                tag="b-button"
            >
                <todo-card
                    :deadline="d"
                    :course="course"
                />
            </b-link>
        </div>
    </div>
</template>

<script>
import todoCard from '@/components/assets/TodoCard.vue'
import { mapGetters, mapMutations } from 'vuex'

export default {
    components: {
        todoCard,
    },
    props: ['deadlines'],
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
            let counter = 0

            function compareDate (a, b) {
                if (!a.deadline) { return 1 }
                if (!b.deadline) { return -1 }
                return new Date(a.deadline) - new Date(b.deadline)
            }

            function compareMarkingNeeded (a, b) {
                if (a.stats.needs_marking + a.stats.unpublished > b.stats.needs_marking + b.stats.unpublished) {
                    return -1
                }
                if (a.stats.needs_marking + a.stats.unpublished < b.stats.needs_marking + b.stats.unpublished) {
                    return 1
                }
                return 0
            }

            function filterTop () {
                return (++counter <= 5)
            }

            function filterNoEntries (assignment) {
                return assignment.totalNeedsMarking !== 0
            }

            const deadlines = this.deadlines.slice()
            if (this.selectedSortOption === 'date') {
                return deadlines.sort(compareDate).filter(filterTop)
            } else if (this.selectedSortOption === 'markingNeeded') {
                return deadlines.sort(compareMarkingNeeded).filter(filterTop).filter(filterNoEntries)
            } else {
                return deadlines.sort(compareDate).filter(filterTop)
            }
        },
    },
    methods: {
        ...mapMutations({
            setSortBy: 'preferences/SET_TODO_SORT_BY',
        }),
        assignmentRoute (cID, aID, jID, isPublished) {
            const route = {
                params: {
                    cID,
                    aID,
                },
            }

            if (!isPublished) { // Teacher not published route
                route.name = 'FormatEdit'
            } else if (this.$hasPermission('can_view_all_journals', 'assignment', aID)) { // Teacher published route
                route.name = 'Assignment'
            } else if (jID === -1) { // Student new group assignment route
                route.name = 'CreateJoinJournal'
            } else { // Student with journal route
                route.name = 'Journal'
                route.params.jID = jID
            }
            return route
        },
    },
}
</script>
