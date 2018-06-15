<template>
    <b-card class="card container-fluid">
        <b-row>
            <b-col cols="3">
                <div class="portrait-container" fluid-grow>
                    <img src="../assets/logo.png">
                </div>
            </b-col>
            <b-col cols="7">
                <progress-bar></progress-bar>
            </b-col>
            <b-col cols="2">
                <todo-circle :num="'200'"></todo-circle>
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
import todoCircle from '@/components/TodoCircle.vue'

export default {
    props: ['student', 'studentNumber', 'studentPortraitPath',
            'studentProgress', 'entryStats'],
    components: {
        'progress-bar': progressBar,
        'todo-circle': todoCircle
    }
}
</script>

<style>

</style>
