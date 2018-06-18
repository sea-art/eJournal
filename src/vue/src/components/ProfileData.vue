<template>
    <b-row>
        <b-col cols="4">
            <img src='../assets/ohno.jpeg'>
        </b-col>
        <b-col cols="8">
            <h7>{{ name }}</h7><br>
            <p class="profile-data">{{ email }}</p>
            <p class="profile-data">{{ id }}</p>
            <p class="profile-data">{{ courses[0].name }}</p>
        </b-col>
    </b-row>
</template>

<script>
import course from '@/api/course'

export default {
    props: ['name', 'email', 'id', 'image'],
    data () {
        return {
            courses: [],
            test: 'hoi'
        }
    },
    created () {
        course.get_user_courses()
            .then(response => { this.courses = response })
            .catch(_ => alert('Error while loading courses'))
    }
}
</script>
