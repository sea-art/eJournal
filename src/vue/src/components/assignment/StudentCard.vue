<template>
    <b-card :class="$root.getBorderClass($route.params.cID)">
        <b-row>
            <b-col order="1" cols="4">
                <img class="img-fluid portrait-max-height" :src="portraitPath">
            </b-col>
            <b-col order="2" cols="8" class="d-none d-sm-inline">
                <todo-square :num="this.stats.submitted - this.stats.graded"/>
                {{ student }}<br/>
                <p>{{ studentNumber }}</p><br/>
                <progress-bar :currentPoints="this.stats.acquired_points" :totalPoints="this.stats.total_points"/>
            </b-col>

            <b-col order="2" cols="8" order-sm="3" sm="3" class="d-sm-none">
                <todo-square v-if="this.stats" :num="this.stats.submitted - this.stats.graded"/>
            </b-col>

            <b-col order="3" cols="12" order-sm="2" sm="5" class="d-sm-none">
                {{ student }}<br/>
                {{ studentNumber }}
            </b-col>

            <b-col order="4" cols="12" sm="8" class="d-sm-none">
                <progress-bar v-if="this.stats" :currentPoints="this.stats.acquired_points" :totalPoints="this.stats.total_points"/>
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
    }
}
</script>

<style lang="sass">
/* TODO Not the most clean solution for xl. */
.portrait-max-height
    max-height: 173px
</style>
