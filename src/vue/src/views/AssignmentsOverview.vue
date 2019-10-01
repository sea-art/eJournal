<template>
    <content-single-column>
        <bread-crumb :currentPage="'Assignments'"/>

        <input
            v-model="searchValue"
            class="theme-input full-width multi-form"
            type="text"
            placeholder="Search..."
        />
        <div class="d-flex">
            <b-form-select
                v-model="selectedSortOption"
                :selectSize="1"
                class="multi-form mr-2"
            >
                <option value="date">
                    Sort by date
                </option>
                <option value="name">
                    Sort by name
                </option>
                <option
                    v-if="$hasPermission('can_add_course')"
                    value="markingNeeded"
                >
                    Sort by marking needed
                </option>
            </b-form-select>
            <b-button
                v-if="!order"
                class="button multi-form"
                @click.stop
                @click="setOrder(!order)"
            >
                <icon name="long-arrow-down"/>
                Ascending
            </b-button>
            <b-button
                v-if="order"
                class="button multi-form"
                @click.stop
                @click="setOrder(!order)"
            >
                <icon name="long-arrow-up"/>
                Descending
            </b-button>
        </div>

        <div
            v-for="(d, i) in computedAssignments"
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
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import todoCard from '@/components/assets/TodoCard.vue'
import assignmentAPI from '@/api/assignment.js'

import { mapGetters, mapMutations } from 'vuex'

export default {
    name: 'AssignmentsOverview',
    components: {
        contentSingleColumn,
        breadCrumb,
        todoCard,
    },
    data () {
        return {
            deadlines: [],
        }
    },
    computed: {
        ...mapGetters({
            order: 'preferences/assignmentOverviewSortAscending',
            getAssignmentSearchValue: 'preferences/assignmentOverviewSearchValue',
            getAssignmentOverviewSortBy: 'preferences/assignmentOverviewSortBy',
        }),
        searchValue: {
            get () {
                return this.getAssignmentSearchValue
            },
            set (value) {
                this.setAssignmentSearchValue(value)
            },
        },
        selectedSortOption: {
            get () {
                return this.getAssignmentOverviewSortBy
            },
            set (value) {
                this.setAssignmentOverviewSortBy(value)
            },
        },
        computedAssignments () {
            const self = this

            function compareName (a, b) {
                return b.name < a.name
            }

            function compareDate (a, b) {
                if (!a.deadline.date) { return 1 }
                if (!b.deadline.date) { return -1 }
                return new Date(a.deadline.date) - new Date(b.deadline.date)
            }

            function compareMarkingNeeded (a, b) {
                return (a.stats.needs_marking + a.stats.unpublished) - (b.stats.needs_marking + b.stats.unpublished)
            }

            function searchFilter (assignment) {
                return assignment.name.toLowerCase().includes(self.getAssignmentSearchValue.toLowerCase())
            }

            const deadlines = this.deadlines.filter(searchFilter)
            if (this.selectedSortOption === 'name') {
                deadlines.sort(compareName)
            } else if (this.selectedSortOption === 'date') {
                deadlines.sort(compareDate)
            } else if (this.selectedSortOption === 'markingNeeded') {
                deadlines.sort(compareMarkingNeeded)
            }

            return this.order ? deadlines.reverse() : deadlines
        },
    },
    created () {
        assignmentAPI.list()
            .then((deadlines) => { this.deadlines = deadlines })
    },
    methods: {
        ...mapMutations({
            setOrder: 'preferences/SET_ASSIGNMENT_OVERVIEW_SORT_ASCENDING',
            setAssignmentSearchValue: 'preferences/SET_ASSIGNMENT_OVERVIEW_SEARCH_VALUE',
            setAssignmentOverviewSortBy: 'preferences/SET_ASSIGNMENT_OVERVIEW_SORT_BY',
        }),
        assignmentRoute (cID, aID, jID, isPublished) {
            const route = {
                params: {
                    cID,
                    aID,
                },
            }

            if (!isPublished) {
                route.name = 'FormatEdit'
            } else if (this.$hasPermission('can_view_all_journals', 'assignment', aID)) {
                route.name = 'Assignment'
            } else {
                route.name = 'Journal'
                route.params.jID = jID
            }
            return route
        },
        compare (a, b) {
            if (a < b) { return this.order ? 1 : -1 }
            if (a > b) { return this.order ? -1 : 1 }
            return 0
        },
    },
}
</script>
