<template>
    <div>
        <h4>
            <b-breadcrumb v-if="$route.params.student != undefined" class="bread-crumb" :items="items.concat(' ')"/>
            <b-breadcrumb v-else-if="$route.params.assign != undefined" class="bread-crumb" :items="items.slice(0, 2).concat(' ')"/>
            <b-breadcrumb v-else-if="$route.params.course != undefined" class="bread-crumb" :items="items.slice(0, 1).concat(' ')"/>
        </h4>
        <h1>
            {{ currentPage }}<br/>
            <!-- {{ this.$route.params.course }} -->
            <!-- {{ this.$route.params.courseName }} -->
        </h1>
    </div>
</template>

<script>
export default {
    props: ['currentPage', 'course'],
    data () {
        return {
            items: [{
                text: 'Courses',
                to: { name: 'Home'}
            },
            {
                text: this.course,
                to: {
                    name: 'Course',
                    params: {
                        course: this.$route.params.course,
                        courseName: this.$route.params.courseName
                    }
                }
            },
            {
                text: this.assign,
                to: {
                    name: 'Assignment',
                    params: {
                        course: this.$route.params.course,
                        assign: this.$route.params.assign,
                        courseName: this.$route.params.courseName,
                        assignmentName: this.$route.params.assignmentName
                    }
                }
            }]
        }
    }
}
</script>

<style>
.bread-crumb {
    padding: 0px;
    background-color: var(--theme-medium-grey);
    margin-bottom: 0px;
}
</style>
