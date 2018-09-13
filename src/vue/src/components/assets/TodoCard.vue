<template>
    <b-card :class="$root.getBorderClass(deadline.course.id)">
        <todo-square v-if="deadline.stats.unpublished" :num="deadline.stats.needs_marking + deadline.stats.unpublished" class="float-right" />
        <h6>{{ $root.beautifyDate(deadline.deadline) }}</h6>
        <h5>{{ deadline.name }}</h5>
        {{ deadline.course.abbreviation }} <br/>
        Due in {{ timeLeft }}

    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    props: ['deadline'],
    components: {
        'todo-square': todoSquare
    },
    computed: {
        timeLeft: function () {
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

            if (days > 0) {
                return days + ' days(s)'
            }
            if (hours > 0) {
                return hours + ' hours(s)'
            }
            if (minutes > 0) {
                return minutes + ' minutes(s)'
            }
        }
    }
}
</script>

<style lang="sass" scoped>
@import "~sass/modules/colors.sass"

h6
    display: inline

p
    text-align: right
    font-size: 20px
    color: $theme-blue
    margin-bottom: 0px
</style>
