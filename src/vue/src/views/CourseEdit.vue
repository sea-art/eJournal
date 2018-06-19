<template>
    <content-columns>
        <h1>Course edit</h1>
        <b-form slot="main-content-column" @submit="onSubmit">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseName" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseAbbreviation" maxlength="8" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseStartYear" type="number" maxlength="4" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.courseEndYear" type="number" maxlength="4" required/>
            <b-button type="submit">Update Settings</b-button>
            <b-button :to="{name: 'Course', params: {cID: this.$route.params.cID, courseName: courseName}}">Back</b-button>

        <br/>
        {{courseName}} <br/>
        {{courseData.courseName}} <br/>
        {{courseData.courseAbbreviation}} <br/>
        {{courseData.courseStartYear}} <br/>
        {{courseData.courseEndYear}} <br/>
    </b-form>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'

export default {
    props: {
        courseName: String
    },
    name: 'CourseEdit',
    data () {
        return {
            courseData: {},
            form: {}
        }
    },
    components: {
        'content-columns': contentColumns
    },
    created () {
        this.courseData = {
            courseName: 'Portfolio Academische Vaardigheden 1',
            courseAbbreviation: 'PAV',
            courseStartYear: '2017',
            courseEndYear: '2018'
        },
        this.form = {
            courseName: this.courseData.courseName,
            courseAbbreviation: this.courseData.courseAbbreviation,
            courseStartYear: this.courseData.courseStartYear,
            courseEndYear: this.courseData.courseEndYear
        }
    },
    methods: {
        onSubmit (evt) {
            this.courseData.courseName = this.form.courseName
            this.courseData.courseAbbreviation = this.form.courseAbbreviation
            this.courseData.courseStartYear = this.form.courseStartYear
            this.courseData.courseEndYear =this.form.courseEndYear
            alert('Submit')
        }
    }
}
</script>
