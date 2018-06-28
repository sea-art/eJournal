<template>
    <div>
        <div v-for="c in courses" :key="c.cID">
            <main-card
                @click.native="connectCourse(c.cID)"
                :line1="c.name"
                :line2="'From - To (years eg: 2017 - 2018)'"
                :color="$root.colors[c.cID % $root.colors.length]">
            </main-card>
        </div>
    </div>
</template>

<script>
import mainCard from '@/components/MainCard.vue'
import courseApi from '@/course.js'

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
