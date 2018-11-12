<template>
    <b-card :class="$root.getBorderClass(course.id)">
        <todo-square
            v-if="deadline.stats && deadline.stats.unpublished"
            :num="deadline.stats.needs_marking + deadline.stats.unpublished"
            class="float-right" />

        <h5>{{ deadline.name }}</h5>
        {{ course.abbreviation }}
        <h6 v-if="this.deadline.deadline">
            Due in {{ timeLeft }}
            <span class="right">{{ $root.beautifyDate(deadline.deadline) }}</span>
        </h6>
    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    props: ['deadline', 'course'],
    components: {
        'todo-square': todoSquare
    },
    computed: {
        timeLeft: function () {
            if (!this.deadline.deadline) { return '' }
            var dateNow = new Date()
            var dateFuture = new Date(this.deadline.deadline.replace(/-/g, '/').replace('T', ' '))

            // get total seconds between the times
            var delta = Math.abs(dateFuture - dateNow) / 1000

            // calculate (and subtract) whole days
            var days = Math.floor(delta / 86400)
            delta -= days * 86400

            // calculate (and subtract) whole hours
            var hours = Math.floor(delta / 3600) % 24
            delta -= hours * 3600

            // calculate (and subtract) whole minutes
            var minutes = Math.floor(delta / 60) % 60
            delta -= minutes * 60

            if (days) {
                return days > 1 ? days + ' days' : '1 day'
            }

            if (hours) {
                return hours > 1 ? hours + ' hours' : '1 hour'
            }

            return minutes > 1 ? minutes + ' minutes' : '1 minute'
        }
    }
}
</script>

<style lang="sass" scoped>
@import "~sass/modules/colors.sass"

.right
    float: right

p
    text-align: right
    font-size: 20px
    color: $theme-blue
    margin-bottom: 0px
</style>
