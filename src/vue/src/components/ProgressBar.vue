<template>
    <b-row>
        <b-col cols="6" lg-cols="6"><h5><b>{{ currentPoints }}</b> Points</h5></b-col>
        <b-col cols="6" lg-cols="6"><h4 class="progress-percentage">{{ progressPercentage }}%</h4></b-col>
        <b-col cols="12" lg-cols="12"><b-progress :value="currentPoints" color="blue" :max="totalPoints" class="progress-bar-box" animated></b-progress></b-col>
    </b-row>
</template>

<script>
export default {
    props: ['currentPoints', 'totalPoints'],
    computed: {
        progressPercentage () {
            return this.currentPoints / this.totalPoints * 100
        }
    }
}
</script>

<style>
.progress-percentage   {
    border: none;
    padding: none;
    text-align: right;
}

.progress-bar-box {
    margin-top: 10px;
    height: 20px;
    background-color: white;
}

.progress-bar {
    background-color: var(--theme-blue) !important;
}
</style>
