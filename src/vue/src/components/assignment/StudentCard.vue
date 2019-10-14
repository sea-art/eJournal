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
                    <img
                        class="no-hover"
                        :src="previewPicture"
                    />
                    <number-badge
                        v-if="markingNeeded + unpublished > 0"
                        :leftNum="markingNeeded"
                        :rightNum="unpublished"
                        :title="squareInfo"
                    />
                </div>
                <div class="student-details list-view">
                    <span>
                        <b>{{ journal.names }}</b>
                        <span v-if="groups">({{ groups }})</span>
                    </span>
                    <!-- {{ journal.students[0].user.username }} -->
                </div>
            </b-col>
            <b-col
                class="mt-2"
                md="5"
            >
                <progress-bar
                    :currentPoints="journal.stats.acquired_points"
                    :totalPoints="assignment.points_possible"
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
                        <b>{{ journal.full_names }}</b>
                        <span v-if="groups">({{ groups }})</span>
                    </span>
                    {{ journal.students.map(s => s.user.username).join(', ') }}
                </div>
            </div>
            <progress-bar
                :currentPoints="journal.stats.acquired_points"
                :totalPoints="assignment.points_possible"
                :comparePoints="assignment && assignment.stats ? assignment.stats.average_points : -1"
            />
        </div>
        <slot/>
    </b-card>
</template>

<script>
import progressBar from '@/components/assets/ProgressBar.vue'
import numberBadge from '@/components/assets/NumberBadge.vue'

export default {
    components: {
        progressBar,
        numberBadge,
    },
    props: {
        assignment: {
            default: null,
            required: true,
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
                student => student.user.profile_picture !== '/static/unknown-profile.png')
            if (studentsWithPicture.length > 0) {
                return studentsWithPicture[0].user.profile_picture
            } else {
                return '/static/unknown-profile.png'
            }
        },
        groups () {
            const groups = []
            this.journal.students.forEach((student) => {
                if (student.user.groups) {
                    student.user.groups.forEach((group) => {
                        if (!groups.includes(group)) {
                            groups.push(group.name)
                        }
                    })
                }
            })
            return groups.join(', ')
        },
        markingNeeded () {
            return this.journal.stats.submitted - this.journal.stats.graded
        },
        unpublished () {
            return this.journal.stats.graded - this.journal.stats.published
        },
        squareInfo () {
            const info = []
            if (this.markingNeeded === 1) {
                info.push('an entry needs marking')
            } else if (this.markingNeeded > 1) {
                info.push(`${this.markingNeeded} entries need marking`)
            }
            if (this.unpublished === 1) {
                info.push('an entry needs to be published')
            } else if (this.unpublished > 1) {
                info.push(`${this.unpublished} grades need to be published`)
            }
            const s = info.join(' and ')
            return `${s.charAt(0).toUpperCase()}${s.slice(1)}`
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
    .number-badge
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
