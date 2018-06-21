<template>
    <content-columns>
        <b-form slot="main-content-column" @submit="onSubmit">
            <h1>{{pageName}}</h1>

            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                     v-model="course.name"
                     placeholder="Course name"
                     required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                     v-model="course.abbr"
                     maxlength="10"
                     placeholder="Course Abbreviation (Max 10 letters)"
                     required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form"
                     v-model="course.date"
                     type="date"
                     required/>

            <b-button type="submit">Update Course</b-button>
            <b-button @click.prevent.stop="deleteCourse()">Delete Course</b-button>
            <b-button :to="{name: 'Course', params: {cID: this.$route.params.cID, courseName: pageName}}">Back</b-button>
        <br/>
    </b-form>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import courseApi from '@/api/course.js'

export default {
    name: 'CourseEdit',
    data () {
        return {
            pageName: '',
            course: {},
            form: {}
        }
    },
    components: {
        'content-columns': contentColumns
    },
    created () {
        courseApi.get_course_data(this.$route.params.cID)
            .then(response => {
                this.course = response
                this.pageName = this.course.name
            })
            .catch(_ => alert('Error while loading course data'))
    },
    methods: {
        onSubmit () {
            courseApi.update_course(this.$route.params.cID,
                this.course.name,
                this.course.abbr,
                this.course.date)
                .then(response => {
                    this.course = response
                    this.pageName = this.course.name
                })
        },
        deleteCourse () {
            if (confirm('Are you sure you want to delete ' + this.course.name + '?')) {
                courseApi.delete_course(this.$route.params.cID)
                    .then(response => {
                        this.$router.push({name: 'Home'})
                    })
            }
        }
    }
}
</script>
