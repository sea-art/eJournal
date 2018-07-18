<template>
    <b-card :class="$root.getBorderClass($route.params.cID)">
        <b-row>
            <b-col order="1" cols="4">
                <img class="img-fluid student-card-portrait" :src="portraitPath">
            </b-col>
            <b-col order="2" cols="8">
                <todo-square v-if="numMarkingNeeded > 0" class="float-right" :num="numMarkingNeeded"/>
                <b>{{ student }}</b><br/>
                {{ studentNumber }}<br/><br/>
                <progress-bar :currentPoints="this.stats.acquired_points" :totalPoints="this.stats.total_points"/>
            </b-col>
        </b-row>
    </b-card>
</template>

<script>
import progressBar from '@/components/assets/ProgressBar.vue'
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    props: ['student', 'studentNumber', 'portraitPath', 'stats'],
    components: {
        'progress-bar': progressBar,
        'todo-square': todoSquare
    },
    computed: {
        numMarkingNeeded () {
            return this.stats.submitted - this.stats.graded
        }
    }
}
</script>

<style lang="sass">
/* TODO Not the most clean solution for xl. */
.student-card-portrait
    border-radius: 50% !important
    display: block
    margin: auto
    max-height: 150px
</style>
