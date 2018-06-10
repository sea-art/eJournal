<template>
    <div class="dashboard">
        <h1>{{ msg }}</h1>

        <div v-for="c in courses">
            <router-link tag="button" :to="{ name: 'Course', params: {course: c[3]} }">
                <course-comp :cName="c[0]" :cAuth="c[1]" :cDate="c[2]"></course-comp>
            </router-link>
        </div>
    </div>
</template>

<script>
import courseCard from '@/components/courseCard.vue'

export default {
    name: 'dashboard',
    data() {
        return {
            msg: "Dashboard",
            courses: [["Webprogrammeren en databases project",
                       "Rob Belleman", "01-01-2017", "WebDB"],
                      ["Academische vaardigheden informatica 2",
                       "Robert van Wijk", "01-01-2017", "PAV"],
                      ["Academische vaardigheden informatica 1",
                       "Robert van Wijk", "01-01-2017", "PAV"]]
        }
    },
    components: {
        'course-comp': courseCard
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
    font-weight: normal;
}
ul {
    list-style-position: inside;
}
a {
    color: #42b983;
}
</style>
