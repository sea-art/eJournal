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
    props: ['lti', 'courses'],
    components: {
        'main-card': mainCard
    },
    methods: {
        connectCourse (cID) {
            courseApi.connect_course_lti(cID, this.lti.ltiCourseID)
                .then(course => { this.$emit('handleAction', course.cID) })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    }
}
</script>
