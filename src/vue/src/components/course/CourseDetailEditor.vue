<template>
    <div>
        <h4 class="mb-2">
            <span>Manage course details</span>
        </h4>
        <b-card
            class="no-hover multi-form"
            :class="$root.getBorderClass($route.params.uID)"
        >
            <b-form @submit.prevent="onSubmit">
                <h2 class="field-heading required">
                    Course name
                </h2>
                <b-input
                    v-model="course.name"
                    class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    :readonly="!$hasPermission('can_edit_course_details')"
                    placeholder="Course name"
                />
                <h2 class="field-heading required">
                    Course abbreviation
                </h2>
                <b-input
                    v-model="course.abbreviation"
                    class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
                    :readonly="!$hasPermission('can_edit_course_details')"
                    maxlength="10"
                    placeholder="Course abbreviation (max 10 characters)"
                />
                <b-row>
                    <b-col cols="6">
                        <h2 class="field-heading required">
                            Start date
                            <tooltip tip="Start date of the course"/>
                        </h2>
                        <flat-pickr
                            v-model="course.startdate"
                            class="multi-form multi-date-input theme-input full-width"
                            :class="{ 'input-disabled': !$hasPermission('can_edit_course_details') }"
                            :config="{
                                maxDate: course.enddate
                            }"
                        />
                    </b-col>
                    <b-col cols="6">
                        <h2 class="field-heading required">
                            End date
                            <tooltip tip="End date of the course"/>
                        </h2>
                        <flat-pickr
                            v-model="course.enddate"
                            class="multi-form multi-date-input theme-input full-width"
                            :class="{ 'input-disabled': !$hasPermission('can_edit_course_details') }"
                            :config="{
                                minDate: course.startdate
                            }"
                        />
                    </b-col>
                </b-row>
                <b-button
                    v-if="$hasPermission('can_edit_course_details')"
                    class="add-button float-right"
                    type="submit"
                >
                    <icon name="save"/>
                    Save
                </b-button>
            </b-form>
        </b-card>
    </div>
</template>

<script>
import tooltip from '@/components/assets/Tooltip.vue'
import courseAPI from '@/api/course.js'

export default {
    name: 'CourseEdit',
    components: {
        tooltip,
    },
    props: {
        course: {
            required: true,
        },
    },
    methods: {
        formFilled () {
            return this.course.name && this.course.abbreviation && this.course.startdate && this.course.enddate
        },
        onSubmit () {
            if (this.formFilled()) {
                courseAPI.update(
                    this.course.id,
                    this.course,
                    { customSuccessToast: 'Successfully updated the course.' },
                )
                    .then((course) => {
                        this.$emit('update-course', course)
                    })
            } else {
                this.$toasted.error('One or more required fields are empty.')
            }
        },
    },
}
</script>
