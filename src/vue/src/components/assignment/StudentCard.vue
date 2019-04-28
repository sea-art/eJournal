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
                    <img :src="previewPicture"/>
                    <todo-square
                        v-if="numMarkingNeeded > 0"
                        :num="numMarkingNeeded"
                    />
                </div>
                <div class="student-details list-view">
                    <span>
                        <b>{{ journal.names }}</b>
                        <span v-if="groups">({{ groups }})</span>
                    </span>
                    {{ journal.students[0].username }}
                </div>
            </b-col>
            <b-col
                class="mt-2"
                md="5"
            >
                <progress-bar
                    :currentPoints="journal.stats.acquired_points"
                    :totalPoints="journal.stats.total_points"
                />
            </b-col>
        </b-row>
        <div v-else>
            <div class="d-flex multi-form">
                <div class="portrait-wrapper">
                    <img :src="previewPicture"/>
                </div>
                <div class="student-details">
                    <span>
                        <b>{{ journal.names }}</b>
                        <span v-if="groups">({{ groups }})</span>
                    </span>
                    {{ students.map(s => s.username).join(', ') }}
                </div>
            </div>
            <progress-bar
                :currentPoints="journal.stats.acquired_points"
                :totalPoints="journal.stats.total_points"
                :comparePoints="assignment && assignment.stats ?
                    assignment.stats.average_points : -1"
            />
        </div>
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
        assignment: {
            default: null,
            required: false,
        },
        journal: {
            required: true,
        },
        listView: {
            default: false,
        },
    },
    computed: {
        numMarkingNeeded () {
            return this.journal.stats.submitted - this.journal.stats.graded
        },
        previewPicture () {
            const studentsWithPicture = this.journal.students.filter(
                student => student.profile_picture !== '/static/unknown-profile.png')
            if (studentsWithPicture.length > 0) {
                return studentsWithPicture[0].profile_picture
            } else {
                return '/static/unknown-profile.png'
            }
        },
        groups () {
            const groups = []
            this.journal.students.forEach((student) => {
                student.groups.forEach((group) => {
                    if (!groups.includes(group)) {
                        groups.push(group.name)
                    }
                })
            })
            return groups.join(', ')
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
