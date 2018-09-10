<template>
    <b-card :class="$root.getBorderClass($route.params.cID)">
        <b-row>
            <b-col order="1" cols="12">
                <todo-square v-if="numMarkingNeeded > 0 && !hideTodo" class="float-right" :num="numMarkingNeeded"/>
                <img class="img-fluid student-card-portrait" :src="student.profile_picture">
                <b>{{ student.first_name + ' ' + student.last_name }}</b><br/>
                {{ student.username }}
                <progress-bar v-if="!fullWidthProgress || $root.mdMax()" :currentPoints="this.stats.acquired_points" :totalPoints="this.stats.total_points"/>
            </b-col>
        </b-row>
        <progress-bar v-if="fullWidthProgress && $root.lg()"
                      :currentPoints="this.stats.acquired_points"
                      :totalPoints="this.stats.total_points"
                      :comparePoints="this.assignment ? this.assignment.stats.average_points : -1"/>
    </b-card>
</template>

<script>
import progressBar from '@/components/assets/ProgressBar.vue'
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    props: {
        'student': {
            required: true
        },
        'stats': {
            required: true
        },
        'hideTodo': {
            type: Boolean,
            default: false
        },
        'fullWidthProgress': {
            type: Boolean,
            default: false
        },
        'assignment': {
            required: false
        }
    },
    components: {
        'progress-bar': progressBar,
        'todo-square': todoSquare
    },
    computed: {
        numMarkingNeeded () {
            return this.stats.submitted - this.stats.graded
        }
    }
}
</script>

<style lang="sass">
@import '~sass/partials/shadows.sass'

.student-card-portrait
    @extend .shadow
    border-radius: 50% !important
    display: block
    margin: auto 32px 10px auto
    max-height: 60px
    float: left
</style>
