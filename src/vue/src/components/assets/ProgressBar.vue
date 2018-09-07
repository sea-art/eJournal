<template>
    <b-row>
        <b-col cols="12">
            <h5 class="progress-percentage"><b>{{ currentPoints }}</b> Points</h5>
            <h4 class="progress-percentage float-right">{{ progressPercentage }}%</h4>
            <p v-if="comparePoints">{{ message }}</p>
        </b-col>
        <b-col cols="12">
            <b-progress class="shadow progress-bar-box" color="white" :max="totalPoints">
                <b-progress-bar class="own-bar"
                                :value="comparePoints === -1 ? currentPoints : Math.min(currentPoints, comparePoints)"/>
                <b-progress-bar class="compare-bar"
                                :value="Math.abs(comparePoints - currentPoints)"
                                v-if="comparePoints !== -1 && comparePoints > currentPoints"/>
                <b-progress-bar class="compare-bar ahead"
                                :value="Math.abs(comparePoints - currentPoints)"
                                v-else-if="comparePoints !== -1"/>
            </b-progress>
        </b-col>
    </b-row>
</template>

<script>
export default {
    props: {
        'currentPoints': {
            required: true
        },
        'totalPoints': {
            required: true
        },
        'comparePoints': {
            default: -1
        }
    },
    data () {
        return {
            aheadClass: 'ahead'
        }
    },
    computed: {
        progressPercentage () {
            return (this.currentPoints / this.totalPoints * 100).toFixed(0)
        },
        difference () {
            return Math.round(Math.abs((this.comparePoints - this.currentPoints) * 100)) / 100
        },
        message () {
            if (this.comparePoints === -1) {
                return null
            }

            let message = 'You are '
            // On average
            if (this.difference === 0) {
                message += 'on average.'
            } else {
                // Ahead or behind
                if (this.comparePoints <= this.currentPoints) {
                    message += 'ahead by '
                } else {
                    message += 'behind by '
                }
                // Multiple or only 1 points
                if (this.difference === 1) {
                    message += '1 point.'
                } else {
                    message += this.difference + ' points.'
                }
            }
            return message
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

.own-bar
    background-color: $theme-blue !important
.compare-bar
    background-color: $theme-orange !important
    &.ahead
        background-color: $theme-green !important
</style>
