<template>
    <div>
        <b-form @submit.prevent="onSubmit" @reset.prevent="onReset" :v-model="form.ltiCourseID">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.courseName" placeholder="Course name" required/>
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.courseAbbr" maxlength="10" placeholder="Course Abbreviation (Max 10 letters)" required/>
            <b-row>
                <b-col cols="6">
                    <b-form-group label="From:">
                        <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form multi-date-input theme-input" v-model="form.courseStartdate" type="date" placeholder="From" required/>
                    </b-form-group>
                </b-col>
                <b-col cols="6">
                    <b-form-group label="To:">
                        <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form multi-date-input theme-input" v-model="form.courseEnddate" type="date" placeholder="To" required/>
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
import courseApi from '@/api/course.js'
import icon from 'vue-awesome/components/Icon'
import genericUtils from '@/utils/generic_utils.js'
import permissionsAPI from '@/api/permissions.js'

export default {
    name: 'CreateCourse',
    props: ['lti'],
    data () {
        return {
            form: {
                courseName: '',
                courseAbbr: '',
                courseStartdate: '',
                courseEnddate: '',
                ltiCourseID: ''
            }
        }
    },
    methods: {
        onSubmit () {
            courseApi.create_new_course(this.form.courseName, this.form.courseAbbr, this.form.courseStartdate,
                this.form.courseEnddate, this.form.ltiCourseID).then(course => {
                if (!this.lti) { // If we are here via LTI a full store update will take place anyway.
                    permissionsAPI.get_course_permissions(course.cID).then(coursePermissions => {
                        this.$store.commit('user/UPDATE_PERMISSIONS', { permissions: coursePermissions, key: 'course' + course.cID })
                    })
                }
                this.$emit('handleAction', course.cID)
            }).catch(error => { this.$toasted.error(error.response.data.description) })
        },
        onReset (evt) {
            this.form.courseName = ''
            this.form.courseAbbr = ''
            this.form.courseStartdate = ''
            this.form.courseEnddate = ''
        }
    },
    mounted () {
        if (this.lti !== undefined) {
            this.form.courseName = this.lti.ltiCourseName
            this.form.courseAbbr = this.lti.ltiCourseAbbr
            this.form.ltiCourseID = this.lti.ltiCourseID
            this.form.courseStartdate = this.lti.ltiCourseStart.split(' ')[0]
            this.form.courseEnddate = genericUtils.yearOffset(this.form.courseStartdate)
        }
    },
    components: {
        icon
    }
}
</script>
