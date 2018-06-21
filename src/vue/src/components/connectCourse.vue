<template>
    <div>
        {{ this.form.courseStartdate }}
        <b-form @submit="onSubmit" @reset="onReset" :v-model="form.ltiCourseID">
            <!-- TODO: Laad alle courses in en maak single selectable! -->
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form>
    </div>
</template>

<script>
import courseApi from '@/api/course.js'

export default {
    name: 'ConnectCourse',
    data () {
        return {
            form: {
                courseName: '',
                courseAbbreviation: '',
                courseStartdate: '',
                ltiCourseID: ''
            }
        }
    },
    methods: {
        onSubmit () {
            courseApi.create_new_course(this.form.courseName, this.form.courseAbbreviation, this.form.courseStartdate, this.form.ltiCourseID)
                .then(_ => { this.$emit('handleAction') })
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.form.courseName = ''
            this.form.courseAbbreviation = ''
            this.form.courseStartdate = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
