<template>
    <b-card class="card container-fluid">
        <b-row>
            <b-col cols="3">
                <div class="portrait-container" fluid-grow>
                    <img :src="studentPortraitPath">
                </div>
            </b-col>
            <b-col cols="7">
                <progress-bar></progress-bar>
            </b-col>
            <b-col cols="2">
                <todo-square :num="this.entryStats.total - this.entryStats.graded">
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
    props: ['student', 'studentNumber', 'studentPortraitPath',
            'studentProgress', 'entryStats'],
    components: {
        'progress-bar': progressBar,
        'todo-square': todoSquare
    }
}
</script>

<style>

</style>
