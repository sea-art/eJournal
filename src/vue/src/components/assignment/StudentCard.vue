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
                        class="theme-img no-hover"
                        :src="student.profile_picture"
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
                        <b>{{ student.full_name }}</b>
                        <span v-if="student.group">({{ student.group }})</span>
                    </span>
                    <span class="username-wrapper">
                        {{ student.username }}
                    </span>
                </div>
            </b-col>
            <b-col
                class="mt-2"
                md="5"
            >
                <progress-bar
                    :currentPoints="stats.acquired_points"
                    :totalPoints="assignment.points_possible"
                />
            </b-col>
        </b-row>
        <div v-else>
            <div class="d-flex multi-form">
                <div class="portrait-wrapper">
                    <img
                        :src="student.profile_picture"
                        class="theme-img"
                    />
                </div>
                <div class="student-details">
                    <span>
                        <b>{{ student.full_name }}</b>
                        <span v-if="student.group">({{ student.group }})</span>
                    </span>
                    <span class="username-wrapper">
                        {{ student.username }}
                    </span>
                </div>
            </div>
            <progress-bar
                :currentPoints="stats.acquired_points"
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
            required: true,
        },
    },
    computed: {
        markingNeeded () {
            return this.stats.submitted - this.stats.graded
        },
        unpublished () {
            return this.stats.graded - this.stats.published
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
    position: relative
    width: calc(100% - 80px)
    min-height: 70px
    flex-direction: column
    padding: 10px
    .username-wrapper
        display: block
        width: 100%
        text-overflow: ellipsis
        white-space: nowrap
        overflow: hidden
    &.list-view
        padding-left: 40px
    @include sm-max
        align-items: flex-end

</style>
