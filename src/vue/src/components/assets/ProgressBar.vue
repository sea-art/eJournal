<template>
    <b-row>
        <b-col cols="12">
            <h5 class="progress-percentage"><b>{{ currentPoints }}</b> Points</h5>
            <h4 class="progress-percentage float-right">{{ progressPercentage }}%</h4>
        </b-col>
        <b-col cols="12"><b-progress :value="currentPoints" color="blue" :max="totalPoints" class="progress-bar-box shadow" animated></b-progress></b-col>
    </b-row>
</template>

<script>
export default {
    props: ['currentPoints', 'totalPoints'],
    computed: {
        progressPercentage () {
            return (this.currentPoints / this.totalPoints * 100).toFixed(0)
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.progress-percentage
    display: inline
    border: none
    padding: 0px !important
    text-align: right

.progress-bar-box
    margin-top: 10px
    height: 20px
    background-color: white

.progress-bar
    background-color: $theme-blue !important
</style>
