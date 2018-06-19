<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseName" placeholder="Course name"/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseAbbreviation" maxlength="10" placeholder="Course Abbreviation (Max 10 letters)"/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseStartdate" type="date"/>
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Submit</b-button>
        </b-form>
    </div>
</template>

<script>
import courseApi from '@/api/course.js'

export default {
    name: 'CreateCourse',
    data () {
        return {
            form: {
                courseName: '',
                courseAbbreviation: '',
                courseStartdate: ''
            }
        }
    },
    methods: {
        onSubmit (evt) {
            courseApi.create_new_course(this.form.courseName, this.form.courseAbbreviation, this.form.courseStartdate)
                .then(response => { console.log(response) })
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
