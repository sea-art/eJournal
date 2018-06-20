<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseName" placeholder="Course name" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseAbbreviation" maxlength="10" placeholder="Course Abbreviation (Max 10 letters)" required/>
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
        onSubmit () {
            courseApi.create_new_course(this.form.courseName, this.form.courseAbbreviation, this.form.courseStartdate)
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
