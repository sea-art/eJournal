<template>
    <div>
        <b-form @submit.prevent="onSubmit" @reset.prevent="onReset" :v-model="form.lti_id">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.name" placeholder="Course name" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.abbreviation" maxlength="10" placeholder="Course Abbreviation (Max 10 letters)" required/>
            <b-row>
                <b-col cols="6">
                    <b-form-group label="From:">
                        <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form multi-date-input theme-input" v-model="form.startdate" type="date" placeholder="From" required/>
                    </b-form-group>
                </b-col>
                <b-col cols="6">
                    <b-form-group label="To:">
                        <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form multi-date-input theme-input" v-model="form.enddate" type="date" placeholder="To" required/>
                    </b-form-group>
                </b-col>
            </b-row>
            <b-button class="float-left change-button" type="reset">
                <icon name="undo"/>
                Reset
            </b-button>
            <b-button class="float-right add-button" type="submit">
                <icon name="plus-square"/>
                Create
            </b-button>
        </b-form>
    </div>
</template>

<script>
import auth from '@/api/auth.js'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'CreateCourse',
    props: ['lti'],
    data () {
        return {
            form: {
                courseName: '',
                courseAbbr: '',
                courseStartdate: this.newDate(0),
                courseEnddate: this.newDate(1),
                ltiCourseID: ''
            }
        }
    },
    methods: {
        onSubmit () {
            auth.create('courses', this.form)
                .then(course => {
                    this.onReset(undefined)
                    this.$emit('handleAction', course.id)
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        onReset (evt) {
            if (evt !== undefined) {
                evt.preventDefault()
            }

            /* Reset our form values */
            this.form.courseName = ''
            this.form.courseAbbr = ''
            this.form.courseStartdate = ''
            this.form.courseEnddate = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        },
        newDate (yearOffset) {
            var date = new Date()
            date.setFullYear(date.getFullYear() + yearOffset)
            return date.toISOString().split('T')[0].slice(0, 10)
        }
    },
    mounted () {
        if (this.lti !== undefined) {
            this.form.courseName = this.lti.ltiCourseName
            this.form.courseAbbr = this.lti.ltiCourseAbbr
            this.form.ltiCourseID = this.lti.ltiCourseID
        }
    },
    components: {
        icon
    }
}
</script>
