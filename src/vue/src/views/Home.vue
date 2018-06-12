<template>
    <b-row>
        <b-col cols="3" class="left-content"></b-col>
        <b-col cols="6" class="main-content">
            <h1>Home Page</h1>
            <div v-for="c in courses" :key="c.cID">
                <b-link tag="b-button" :to="{ name: 'Course', params: {course: c.cID} }">
                    <main-card :line1="c.name" :line2="c.date"> <!-- Enter obj3 --> </main-card>
                </b-link>
            </div>
        </b-col>
        <b-col cols="3" class="right-content"></b-col>
    </b-row>
</template>

<script>
import mainCard from '@/components/MainCard.vue'
import course from '@/api/course'

export default {
    name: 'Home',
    data () {
        return {
            courses: course.get_user_courses()
        }
    },
    components: {
        'main-card': mainCard
    }
}
</script>
