<template>
    <b-card :class="$root.getBorderClass(course.id)">
        <todo-square
            v-if="deadline.stats && deadline.stats.unpublished"
            :num="deadline.stats.needs_marking + deadline.stats.unpublished"
            class="float-right" />

        <b class="deadline-name field-heading">{{ deadline.name }}</b> ({{ course.abbreviation }})
        <b-badge
            v-if="!deadline.is_published"
            class="ml-2 mt-2">
            Unpublished
        </b-badge>
        <br />

        <span v-if="this.deadline.deadline">
            <!-- Teacher deadline shows last submitted entry date  -->
            <span v-if="this.deadline.stats.needs_marking + deadline.stats.unpublished">
                <icon name="eye" class="fill-grey shift-up-3"/> {{ timeLeft[1] }} ago<br/>
            </span>
            <!-- Student deadline shows last not submitted deadline -->
            <span v-else>
                <icon name="calendar" class="fill-grey shift-up-3"/>
                <span v-if="timeLeft[0] < 0">Due in {{ timeLeft[1] }}<br/></span>
                <span v-else class="text-red">{{ timeLeft[1] }} late<br/></span>
            </span>
            <icon name="flag" class="fill-grey shift-up-3"/> {{ $root.beautifyDate(this.deadline.deadline) }}
        </span>
    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['deadline', 'course'],
    components: {
        'todo-square': todoSquare,
        icon
    },
    computed: {
        timeLeft: function () {
            if (!this.deadline.deadline) { return '' }
            let dateNow = new Date()
            let dateFuture = new Date(this.deadline.deadline)

            // get total seconds between the times
            let delta = Math.abs(dateFuture - dateNow) / 1000
            let dir = dateNow - dateFuture

            // calculate (and subtract) whole days
            let days = Math.floor(delta / 86400)
            delta -= days * 86400

            // calculate (and subtract) whole hours
            let hours = Math.floor(delta / 3600) % 24
            delta -= hours * 3600

            // calculate (and subtract) whole minutes
            let minutes = Math.floor(delta / 60) % 60
            delta -= minutes * 60

            if (days) {
                return [dir, days > 1 ? days + ' days' : '1 day']
            }

            if (hours) {
                return [dir, hours > 1 ? hours + ' hours' : '1 hour']
            }

            return [dir, minutes > 1 ? minutes + ' minutes' : '1 minute']
        }
    }
}
</script>

<style lang="sass" scoped>
@import "~sass/modules/colors.sass"
@import "~sass/partials/colors.sass"

.deadline-name
    display: inline-block
</style>
