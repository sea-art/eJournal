<template>
    <b-row no-gutters>
        <b-col lg="3" order="3" order-lg="1" class="left-content d-none d-lg-block"></b-col>
        <b-col md="12" lg="6" order="2" class="main-content">
            <bread-crumb :links="['test', 'test2']" :currentPage="'Courses'"></bread-crumb>

            <div v-for="c in courses" :key="c.cID">
                <b-link tag="b-button" :to="{name: 'Course', params: {course: c.cID}}">
                    <main-card :line1="c.name" :line2="c.date" :color="set_color()">hoi</main-card>
                </b-link>
            </div>
        </b-col>
        <b-col md="12" lg="3" order="1" order-lg="3" class="right-content">
            <div v-for="d in deadlines" :key="d.dID">
                <b-link tag="b-button" :to="{name: 'Assignment', params: {course: d.cID[0], assign: d.dID}}">
                    <todo-card :line0="d.datetime" :line1="d.name" :line2="d.course" :color="set_color()">hoi</todo-card>
                </b-link>
            </div>
        </b-col>
    </b-row>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import todoCard from '@/components/TodoCard.vue'
import course from '@/api/course'

export default {
    name: 'Home',
    data () {
        return {
            /* Define the banner colors and set the index to -1 for first setup. */
            colors: ['pink-border', 'peach-border', 'blue-border'],
            color_idx: -1,
            courses: []
        }
    },
    methods: {
        set_color () {
            this.color_idx + 1 === this.colors.length ? this.color_idx = 0 : this.color_idx++
            return this.colors[this.color_idx]
        }
    },
    components: {
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'todo-card': todoCard
    },
    created () {
        course.get_user_courses().then(response => {
            this.courses = response
        })
    }
}
</script>