<template>
    <b-card :class="$root.getBorderClass(course.id)">
        <todo-square
            v-if="deadline.stats && deadline.stats.unpublished"
            :num="deadline.stats.needs_marking + deadline.stats.unpublished"
            class="float-right"
        />

        <b class="field-heading">{{ deadline.name }}</b> ({{ course.abbreviation }})
        <b-badge
            v-if="!deadline.is_published"
            class="ml-2 mt-2"
        >
            Unpublished
        </b-badge>

        <span v-if="deadline.deadline">
            <hr style="margin: 5px 0px"/>
            <!-- Teacher deadline shows last submitted entry date  -->
            <span v-if="deadline.stats.needs_marking + deadline.stats.unpublished">
                <icon
                    name="eye"
                    class="fill-grey shift-up-3"
                /> {{ timeLeft[1] }} ago<br/>
            </span>
            <!-- Student deadline shows last not submitted deadline -->
            <span v-else>
                <icon
                    name="calendar"
                    class="fill-grey shift-up-3 mr-1"
                />
                <span v-if="timeLeft[0] < 0">Due in {{ timeLeft[1] }}<br/></span>
                <span
                    v-else
                    class="text-red"
                >{{ timeLeft[1] }} late<br/></span>
            </span>
            <icon
                name="flag"
                class="fill-grey shift-up-3"
            /> {{ $root.beautifyDate(deadline.deadline) }}
        </span>
    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    components: {
        todoSquare,
    },
    props: ['deadline', 'course'],
    computed: {
        timeLeft () {
            if (!this.deadline.deadline) { return '' }
            const dateNow = new Date()
            const dateFuture = new Date(this.deadline.deadline)

            // get total seconds between the times
            let delta = Math.abs(dateFuture - dateNow) / 1000
            const dir = dateNow - dateFuture

            // calculate (and subtract) whole days
            const days = Math.floor(delta / 86400)
            delta -= days * 86400

            // calculate (and subtract) whole hours
            const hours = Math.floor(delta / 3600) % 24
            delta -= hours * 3600

            // calculate (and subtract) whole minutes
            const minutes = Math.floor(delta / 60) % 60
            delta -= minutes * 60

            if (days) {
                return [dir, days > 1 ? `${days} days` : '1 day']
            }

            if (hours) {
                return [dir, hours > 1 ? `${hours} hours` : '1 hour']
            }

            return [dir, minutes > 1 ? `${minutes} minutes` : '1 minute']
        },
    },
}
</script>
