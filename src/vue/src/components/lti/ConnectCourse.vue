<template>
    <div>
        <div v-for="c in courses" :key="c.cID">
            <main-card
                @click.native="connectCourse(c.cID)"
                :line1="c.name"
                :line2="c.startdate.substring(0, 4) + '-' + c.enddate.substring(0, 4)">
            </main-card>
        </div>
    </div>
</template>

<script>
import mainCard from '@/components/assets/MainCard.vue'
import courseApi from '@/api/course.js'

export default {
    name: 'ConnectCourse',
    props: ['lti'],
    components: {
        'main-card': mainCard
    },
    data () {
        return {
            courses: []
        }
    },
    methods: {
        loadCourses () {
            courseApi.get_user_teacher_courses()
                .then(response => { this.courses = response })
        },
        connectCourse (cID) {
            courseApi.connect_course_lti(cID, this.lti.ltiCourseID)
                .then(response => { this.$emit('handleAction', response.cID) })
        }
    },
    created () {
        this.loadCourses()
    }
}
</script>
