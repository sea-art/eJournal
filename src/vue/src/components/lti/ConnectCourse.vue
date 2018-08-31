<template>
    <div>
        <div v-for="c in courses" :key="c.id">
            <main-card
                @click.native="connectCourse(c.id)"
                :line1="c.name"
                :line2="c.startdate.substring(0, 4) + '-' + c.enddate.substring(0, 4)">
            </main-card>
        </div>
    </div>
</template>

<script>
import mainCard from '@/components/assets/MainCard.vue'
import courseAPI from '@/api/course'

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
            courseAPI.getLinkable()
                .then(courses => { this.courses = courses })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        connectCourse (cID) {
            courseAPI.update(cID, {lti_id: this.lti.ltiCourseID})
                .then(course => { this.$emit('handleAction', course.id) })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    },
    created () {
        this.loadCourses()
    }
}
</script>
