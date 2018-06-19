<template>
    <b-card class="card container-fluid" :class="color">
        <b-row>
            <b-col cols="3">
                <div class="portrait-container" fluid-grow>
                    <img :src="portraitPath">
                </div>
            </b-col>
            <b-col cols="7">
                <progress-bar :currentPoints="this.stats.acquired_points" :totalPoints="this.stats.total_points">
                </progress-bar>
            </b-col>
            <b-col cols="2">
                <todo-square :num="this.stats.submitted - this.stats.graded">
                </todo-square>
            </b-col>
        </b-row>
        <b-row>
            {{ studentNumber }}: {{ student }}
        </b-row>
    </b-card>
</template>

<script>
import progressBar from '@/components/ProgressBar.vue'
import todoSquare from '@/components/TodoSquare.vue'

export default {
    props: ['student', 'studentNumber', 'portraitPath', 'stats', 'color'],
    components: {
        'progress-bar': progressBar,
        'todo-square': todoSquare
    }
}
</script>

<style>

</style>
