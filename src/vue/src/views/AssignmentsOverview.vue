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
        <load-wrapper :loading="loadingAssignments">
            <div
                v-for="(d, i) in computedAssignments"
                :key="i"
            >
                <b-link
                    v-if="d.course"
                    :to="assignmentRoute(d)"
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
            <main-card
                v-if="computedAssignments.length === 0"
                line1="No assignments found"
                line2="You currently do not participate in any assignments."
                class="no-hover border-dark-grey"
            />
        </load-wrapper>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import loadWrapper from '@/components/loading/LoadWrapper.vue'
import todoCard from '@/components/assets/TodoCard.vue'
import mainCard from '@/components/assets/MainCard.vue'
import assignmentAPI from '@/api/assignment.js'

import { mapGetters, mapMutations } from 'vuex'

export default {
    name: 'AssignmentsOverview',
    components: {
        contentSingleColumn,
        breadCrumb,
        loadWrapper,
        todoCard,
        mainCard,
    },
    data () {
        return {
            deadlines: [],
            loadingAssignments: true,
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
            .then((deadlines) => {
                this.deadlines = deadlines
                this.loadingAssignments = false
            })
    },
    methods: {
        ...mapMutations({
            setOrder: 'preferences/SET_ASSIGNMENT_OVERVIEW_SORT_ASCENDING',
            setAssignmentSearchValue: 'preferences/SET_ASSIGNMENT_OVERVIEW_SEARCH_VALUE',
            setAssignmentOverviewSortBy: 'preferences/SET_ASSIGNMENT_OVERVIEW_SORT_BY',
        }),
        assignmentRoute (assignment) {
            const route = {
                params: {
                    cID: assignment.course.id,
                    aID: assignment.id,
                },
            }

            if (this.$hasPermission('can_view_all_journals', 'assignment', assignment.id)) {
                if (!assignment.isPublished) { // Teacher not published route
                    route.name = 'FormatEdit'
                } else { // Teacher published route
                    route.name = 'Assignment'
                }
            } else {
                if (assignment.is_group_assignment && assignment.journal === null) {
                    // Student new group assignment route
                    route.name = 'JoinJournal'
                } else { // Student with journal route
                    route.name = 'Journal'
                    route.params.jID = assignment.journal
                }
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
