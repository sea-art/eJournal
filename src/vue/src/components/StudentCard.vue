<template>
    <b-card class="card container-fluid" :class="color">
        <b-row>
            <b-col cols="3">
                <div class="portrait-container" fluid-grow>
                    <img :src="portraitPath">
                </div>
            </b-col>
            <b-col cols="7">
                <progress-bar :currentPoints="this.progress.acquired" :totalPoints="this.progress.total">
                </progress-bar>
            </b-col>
            <b-col cols="2">
                <todo-square :num="this.stats.total - this.stats.graded">
                </todo-square>
            </b-col>
        </b-row>
        <b-row>
            {{ student }}<br>
            {{ studentNumber }}
        </b-row>
    </b-card>
</template>

<script>
import progressBar from '@/components/ProgressBar.vue'
import todoSquare from '@/components/TodoSquare.vue'

export default {
    props: ['student', 'studentNumber', 'portraitPath', 'progress', 'stats', 'color'],
    components: {
        'progress-bar': progressBar,
        'todo-square': todoSquare
    }
}
</script>

<style>

</style>
