<template>
    <content-columns>
        <h1>Course creation</h1>
        <b-form slot="main-content-column" @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseName" placeholder="Course name" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseAbbreviation" maxlength="8" placeholder="Course Abbreviation (Max 8 letters)" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseStartYear" type="number" maxlength="4" placeholder="Starting year of the course" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseEndYear" type="number" maxlength="4" placeholder="Final year of the course" required/>
            <b-button type="submit">Submit</b-button>
            <b-button type="reset">Reset</b-button>
        </b-form>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'

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
        'content-columns': contentColumns
    },
    methods: {
        onSubmit (evt) {
            alert('Submit')
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.form.courseName = ''
            this.form.courseAbbreviation = ''
            this.form.courseStartYear = ''
            this.form.courseEndYear = ''
            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
