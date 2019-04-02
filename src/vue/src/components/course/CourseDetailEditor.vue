<template>
<div>
  <h4 class="mb-2"><span>Manage course details</span></h4>
  <b-card class="no-hover multi-form" :class="$root.getBorderClass($route.params.uID)">
    <b-form @submit.prevent="onSubmit">
      <h2 class="field-heading required">Course name</h2>
      <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" :readonly="!$hasPermission('can_edit_course_details')" v-model="course.name" placeholder="Course name" />
      <h2 class="field-heading required">Course abbreviation</h2>
      <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" :readonly="!$hasPermission('can_edit_course_details')" v-model="course.abbreviation" maxlength="10" placeholder="Course abbreviation (max 10 characters)" />
      <b-row>
        <b-col xs="6">
          <h2 class="field-heading required">
            From
            <tooltip tip="Start date of the course" />
          </h2>
          <flat-pickr class="multi-form theme-input full-width" :class="{ 'input-disabled': !$hasPermission('can_edit_course_details') }" v-model="course.startdate" />
        </b-col>
        <b-col xs="6">
          <h2 class="field-heading required">
            To
            <tooltip tip="End date of the course" />
          </h2>
          <flat-pickr class="multi-form theme-input full-width" :class="{ 'input-disabled': !$hasPermission('can_edit_course_details') }" v-model="course.enddate" />
        </b-col>
      </b-row>
      <b-button class="add-button float-right" type="submit" v-if="$hasPermission('can_edit_course_details')">
        <icon name="save" />
        Save
      </b-button>
    </b-form>
  </b-card>
</div>
</template>

<script>
import tooltip from '@/components/assets/Tooltip.vue'
import icon from 'vue-awesome/components/Icon'
import courseAPI from '@/api/course'

export default {
    name: 'CourseEdit',
    props: {
        course: {
            required: true
        }
    },
    components: {
        tooltip,
        icon
    },
    methods: {
        formFilled () {
            return this.course.name && this.course.abbreviation && this.course.startdate && this.course.enddate
        },
        onSubmit () {
            if (this.formFilled()) {
                courseAPI.update(this.course.id, this.course, {customSuccessToast: 'Successfully updated the course.'})
                    .then(course => {
                        this.$emit('update-course', course)
                    })
            } else {
                this.$toasted.error('One or more required fields are empty.')
            }
        }
    }
}
</script>
