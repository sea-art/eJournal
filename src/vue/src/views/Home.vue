<template>
    <div class="container-fluid">
        <b-row>
            <b-col3 class="left-content"></b-col3>
            <b-col6 class="main-content">
                <h1>Home</h1>

                <div v-for="c in courses">
                    <b-link tag="b-button" :to="{ name: 'Course', params: {course: c.cID} }">
                        <course-comp :course="c"></course-comp>
                    </b-link>
                </div>
            </b-col6>
            <b-col3 class="right-content">1/4</b-col3>
        </b-row>
    </div>
</template>

<script>
import courseCard from '@/components/courseCard.vue'

export default {
    data() {
        return {
            courses: [{name: "Webprogrammeren en databases project",
                       auth: "Rob Belleman", date: "01-01-2017",
                       abbr: "WDB7", cID: "2017WDB"},
                      {name: "Academische vaardigheden informatica 2",
                       auth: "Robert van Wijk", date: "01-01-2017",
                       abbr: "AVI2", cID: "2017AVI2"},
                      {name: "Academische vaardigheden informatica 1",
                       auth: "Robert van Wijk", date: "01-01-2017",
                       abbr: "AVI1", cID: "2017AVI1"}]
        }
    },
    components: {
        'course-comp': courseCard
    }
}
</script>
