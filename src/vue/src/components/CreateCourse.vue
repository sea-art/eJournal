<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset" :v-model="form.ltiCourseID">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseName" placeholder="Course name" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseAbbr" maxlength="10" placeholder="Course Abbreviation (Max 10 letters)" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseStartdate" type="date" required/>
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form>
    </div>
</template>

<script>
import courseApi from '@/api/course.js'

export default {
    name: 'CreateCourse',
    props: ['lti'],
    data () {
        return {
            form: {
                courseName: '',
                courseAbbr: '',
                courseStartdate: '',
                ltiCourseID: ''
            }
        }
    },
    methods: {
        onSubmit () {
            courseApi.create_new_course(this.form.courseName,
                this.form.courseAbbr, this.form.courseStartdate,
                this.form.ltiCourseID)
                .then(response => { this.$emit('handleAction', response.course.cID) })
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.form.courseName = ''
            this.form.courseAbbr = ''
            this.form.courseStartdate = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    },
    mounted () {
        if (this.lti !== undefined) {
            this.form.courseName = this.lti.ltiCourseName
            this.form.courseAbbr = this.lti.ltiCourseAbbr
            this.form.ltiCourseID = this.lti.ltiCourseID
        }
    }
}
</script>
