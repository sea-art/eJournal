<template>
    <b-card :class="$root.getBorderClass($route.params.cID)">
        <b-row
            v-if="listView"
            noGutters
        >
            <b-col
                class="d-flex"
                md="7"
            >
                <div class="portrait-wrapper">
                    <img :src="student.profile_picture"/>
                    <todo-square
                        v-if="numMarkingNeeded > 0"
                        :num="numMarkingNeeded"
                    />
                </div>
                <div class="student-details list-view">
                    <span>
                        <b>{{ student.full_name }}</b>
                        <span v-if="student.group">({{ student.group }})</span>
                    </span>
                    {{ student.username }}
                </div>
            </b-col>
            <b-col
                class="mt-2"
                md="5"
            >
                <progress-bar
                    :currentPoints="stats.acquired_points"
                    :totalPoints="stats.total_points"
                />
            </b-col>
        </b-row>
        <div v-else>
            <div class="d-flex multi-form">
                <div class="portrait-wrapper">
                    <img :src="student.profile_picture"/>
                </div>
                <div class="student-details">
                    <span>
                        <b>{{ student.full_name }}</b>
                        <span v-if="student.group">({{ student.group }})</span>
                    </span>
                    {{ student.username }}
                </div>
            </div>
            <progress-bar
                :currentPoints="stats.acquired_points"
                :totalPoints="stats.total_points"
                :comparePoints="assignment && assignment.stats ? assignment.stats.average_points : -1"
            />
        </div>
        <slot/>
    </b-card>
</template>

<script>
import progressBar from '@/components/assets/ProgressBar.vue'
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    components: {
        progressBar,
        todoSquare,
    },
    props: {
        student: {
            required: true,
        },
        stats: {
            required: true,
        },
        listView: {
            default: false,
        },
        assignment: {
            default: null,
            required: false,
        },
    },
    computed: {
        numMarkingNeeded () {
            return this.stats.submitted - this.stats.graded
        },
    },
}
</script>

<style lang="sass">
@import '~sass/partials/shadows.sass'
@import '~sass/modules/breakpoints.sass'

.portrait-wrapper
    position: relative
    min-width: 80px
    height: 70px
    img
        @extend .shadow
        width: 70px
        height: 70px
        border-radius: 50% !important
    .todo-square
        position: absolute
        right: 0px
        top: 0px

.student-details
    min-height: 70px
    display: flex
    flex-direction: column
    flex-grow: 1
    padding: 10px
    &.list-view
        padding-left: 40px
    @include sm-max
        align-items: flex-end
</style>
