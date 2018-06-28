<template>
    <b-card class="card" :class="color">
        <b-row>
            <b-col cols="7">
                <h6>{{ date }} {{ hours }}:{{ minutes }}</h6>
            </b-col>
            <b-col cols="5">
                <p>{{ new Date().getFullDay }}</p>
                {{this.$route.path !='/AssignmentsOverview'}}
                <p v-if="this.$root.canAddCourse() && this.$route.path !='/AssignmentsOverview'">
                    <todo-square :num="totalNeedsMarking"/>
                </p>
            </b-col>
        </b-row>
            <h5>{{ name }}</h5>
            {{ abbr }}
    </b-card>
</template>

<script>
import todoSquare from '@/components/TodoSquare.vue'

export default {
    props: ['date', 'hours', 'minutes', 'name', 'abbr', 'totalNeedsMarking', 'color'],
    components: {
        'todo-square': todoSquare
    }
}
</script>

<style scoped>
h6 {
    display: inline;
}

p {
    text-align: right;
    font-size: 20px;
    color: var(--theme-blue);
    margin-bottom: 0px;
}
</style>
