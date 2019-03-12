<template>
    <div>
        <h5 class="progress-percentage">{{ progressPercentage }}%</h5>
        <h5>
            <b>{{ currentPoints ? currentPoints : 0 }}</b> Points
            <tooltip v-if="bonusPoints != 0" :tip="(currentPoints - bonusPoints) + ' journal points + ' + bonusPoints + ' bonus points'" />
        </h5>
        <b-progress class="progress-bar-box multi-form" color="white" :max="totalPoints">
            <b-progress-bar class="own-bar"
                            :value="zeroIfNull(comparePoints === -1 ? currentPoints : Math.min(currentPoints, comparePoints))"/>
            <b-progress-bar class="compare-bar"
                            :value="Math.abs(comparePoints - currentPoints)"
                            v-if="comparePoints !== -1 && comparePoints > currentPoints"/>
            <b-progress-bar class="compare-bar ahead"
                            :value="Math.abs(comparePoints - currentPoints)"
                            v-else-if="comparePoints !== -1"/>
        </b-progress>
        <span v-if="bonusPoints != 0">
            <icon name="star" class="fill-orange shift-up-2"/>
            <b>{{ bonusPoints }}</b> bonus {{ bonusPoints > 1 ? "points" : "point" }}<br/>
        </span>
        <span v-if="comparePoints >= 0">
            <icon name="signal" class="shift-up-2" :class="compareClass"/>
            {{ message }}
        </span>
    </div>
</template>

<script>
import tooltip from '@/components/assets/Tooltip.vue'
import icon from 'vue-awesome/components/Icon'

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
        },
        'bonusPoints': {
            default: 0
        }
    },
    methods: {
        zeroIfNull (val) {
            return (val === null) ? 0 : val
        }
    },
    computed: {
        progressPercentage () {
            return this.zeroIfNull(this.currentPoints / this.totalPoints * 100).toFixed(0)
        },
        difference () {
            return Math.round(Math.abs((this.comparePoints - this.currentPoints) * 100)) / 100
        },
        message () {
            if (this.comparePoints === -1) {
                return null
            }
            var message = ''

            // On average
            if (this.difference === 0) {
                message += 'Same as average'
            } else {
                if (this.difference === 1) {
                    message += '1 point '
                } else {
                    message += this.difference + ' points '
                }
                // Ahead or behind
                if (this.comparePoints <= this.currentPoints) {
                    message += 'above average'
                } else {
                    message += 'below average'
                }
            }
            return message
        },
        compareClass () {
            if (this.difference === 0) {
                return 'fill-grey'
            } else if (this.comparePoints <= this.currentPoints) {
                return 'fill-green'
            }

            return 'fill-red'
        }
    },
    components: {
        tooltip,
        icon
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.progress-percentage
    float: right
    color: $theme-blue
    font-weight: bold

.progress-bar-box
    margin-top: 5px
    height: 15px
    background-color: $theme-light-grey
    border: 1px solid $theme-dark-grey
    border-radius: 5px !important

.own-bar
    background-color: $theme-blue !important
.compare-bar
    background-color: $theme-orange !important
    &.ahead
        background-color: $theme-green !important
</style>
