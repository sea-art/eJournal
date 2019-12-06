<template>
    <b-modal
        :id="modalID"
        size="lg"
        title="Copy assignment"
        hideFooter
    >
        <b-card class="no-hover">
            <h2 class="multi-form">
                Select an assignment to copy
            </h2>
            <p>
                This action will create a new assignment that is identical to the assignment of your choice.
                Existing journals are not copied and will remain accessible only from the original assignment.
            </p>

            <div
                v-for="copyable in copyableFormats"
                :key="`copyable-${copyable.course.id}`"
            >
                <main-card
                    :key="`course-${copyable.course.id}-copy`"
                    :line1="copyable.course.name"
                    :line2="copyable.course.startdate ? (copyable.course.startdate.substring(0, 4) +
                        (copyable.course.enddate ? ` - ${copyable.course.enddate.substring(0, 4)}` : '')) : ''"
                    @click.native="selectedCourse = copyable.course.id"
                />
                <div
                    v-if="selectedCourse === copyable.course.id"
                    class="pl-5"
                >
                    <assignment-card
                        v-for="assignment in copyable.assignments"
                        :key="`course-${copyable.course.id}-assignment-${assignment.id}-copy`"
                        :assignment="assignment"
                        :class="{
                            active: selectedAssignment === assignment.id,
                            'no-hover': selectedAssignment === assignment.id,
                        }"
                        @click.native="
                            selectedAssignment = (selectedAssignment !== assignment.id) ? assignment.id : null"
                    />
                </div>
            </div>
            <div v-if="!copyableFormats">
                <h4>No existing assignments available</h4>
                <hr class="m-0 mb-1"/>
                Only assignments where you have permission to edit are available for copy.
            </div>

            <div v-if="selectedAssignment !== null">
                <hr/>
                <b-form
                    class="full-width"
                    @submit="copyAssignment"
                >
                    <b-button
                        v-if="!shiftCopyDates"
                        class="multi-form mr-3"
                        @click="shiftCopyDates = true"
                    >
                        <icon name="calendar"/>
                        Shift Deadlines
                    </b-button>
                    <b-button
                        v-else
                        class="multi-form mr-3"
                        @click="shiftCopyDates = false"
                    >
                        <icon name="calendar"/>
                        Keep existing deadlines
                    </b-button>

                    <div
                        v-if="shiftCopyDates"
                        class="shift-deadlines-input"
                    >
                        <icon
                            v-b-tooltip.hover="'The weekdays of the deadlines will be kept intact'"
                            name="info-circle"
                        />
                        Dates will be shifted by
                        <b-form-input
                            id="months"
                            v-model="months"
                            type="number"
                            class="theme-input"
                        />
                        months
                    </div>

                    <b-button
                        class="add-button float-right"
                        type="submit"
                    >
                        <icon name="file"/>
                        Copy
                    </b-button>
                </b-form>
            </div>
        </b-card>
    </b-modal>
</template>

<script>
import assignmentCard from '@/components/assignment/AssignmentCard.vue'
import mainCard from '@/components/assets/MainCard.vue'

import assignmentAPI from '@/api/assignment.js'

export default {
    components: {
        assignmentCard,
        mainCard,
    },
    props: {
        modalID: {
            required: true,
        },
        cID: {
            required: true,
        },
        lti: {
            default: () => { return {} },
            required: false,
        },
    },
    data () {
        return {
            selectedCourse: null,
            selectedAssignment: null,
            copyableFormats: [],
            assignmentCopyInFlight: false,
            shiftCopyDates: true,
            months: 0,
        }
    },
    created () {
        assignmentAPI.getCopyable()
            .then((data) => {
                this.copyableFormats = data
            })
    },
    methods: {
        copyAssignment (e) {
            e.preventDefault()

            if (!this.assignmentCopyInFlight && this.selectedAssignment) {
                this.assignmentCopyInFlight = true
                assignmentAPI.copy(this.selectedAssignment, {
                    course_id: this.cID,
                    months_offset: (!this.shiftCopyDates || this.months === '') ? 0 : this.months,
                    lti_id: this.lti.ltiAssignID,
                }, { customSuccessToast: 'Assignment succesfully copied!' }).then((response) => {
                    this.assignmentCopyInFlight = false

                    this.$store.commit('user/COPY_ASSIGNMENT_PERMISSIONS', {
                        sourceAssignmentID: this.selectedAssignment,
                        copyAssignmentID: response.assignment_id,
                    })

                    this.$router.push({
                        name: 'FormatEdit',
                        params: {
                            cID: this.cID,
                            aID: response.assignment_id,
                        },
                    })
                }).catch((error) => {
                    this.assignmentCopyInFlight = false
                    throw error
                })
            }
        },
    },
}
</script>

<style lang="sass">
.shift-deadlines-input
    font-weight: bold
    color: grey
    margin-bottom: 10px
    display: inline-block
    .theme-input
        display: inline-block
        width: 4em
    svg
        margin-top: -5px
        fill: grey
</style>
