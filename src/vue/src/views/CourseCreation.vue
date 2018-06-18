<template>
    <content-single-columns>
        <h1>Course creation</h1>
        <b-form slot="main-content-column" @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseName" placeholder="Course name"/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseAbbreviation" maxlength="8" placeholder="Course Abbreviation (Max 10 letters)"/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseStartdate" type="date" placeholder="Startdate of the year"/>
            <b-button type="submit">Submit</b-button>
            <b-button type="reset">Reset</b-button>
        </b-form>
    </content-single-columns>
</template>

<script>
import ContentSingleColumn from '@/components/ContentSingleColumn.vue'
import courseApi from '@/api/course.js'

export default {
    name: 'CourseCreation',
    data () {
        return {
            form: {
                courseName: '',
                courseAbbreviation: '',
                courseStartYear: '',
                courseEndYear: ''
            }
        }
    },
    components: {
        'content-single-columns': ContentSingleColumn
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
            this.form.courseEndYear = ''
            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
