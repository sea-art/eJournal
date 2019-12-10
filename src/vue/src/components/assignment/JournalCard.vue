<template>
    <b-card :class="$root.getBorderClass(journal.id)">
        <b-row
            v-if="!editJournal"
            noGutters
        >
            <b-col
                class="d-flex"
                :md="$hasPermission('can_view_all_journals') ? 7 : 12"
            >
                <div class="portrait-wrapper">
                    <img
                        class="no-hover"
                        :src="journal.image"
                    />
                    <number-badge
                        v-if="$hasPermission('can_view_all_journals') && markingNeeded + unpublished > 0"
                        :leftNum="markingNeeded"
                        :rightNum="unpublished"
                        :title="squareInfo"
                    />
                </div>
                <div class="student-details">
                    <b
                        class="max-one-line"
                        :title="journal.name"
                    >
                        {{ journal.name }}
                    </b>
                    <span
                        class="max-one-line"
                        :title="journalAuthors"
                    >
                        <b
                            v-if="journal.author_limit > 1"
                            class="text-grey"
                        >
                            ({{ journal.authors.length }}/{{ journal.author_limit }})
                        </b>
                        {{ journalAuthors }}
                    </span>
                </div>
            </b-col>
            <b-col
                v-if="$hasPermission('can_view_all_journals')"
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
                    <img
                        class="no-hover"
                        :src="journal.image"
                    />
                </div>
                <div class="student-details">
                    <h4>{{ journal.name }}</h4>
                    <draggable
                        class="list-group"
                        :list="journal.authors"
                        group="journals"
                        @change="log"
                    >
                        <student-card
                            v-for="author in journal.authors"
                            :key="author.user.id"
                            :user="author.user"
                        >
                            <div class="handle d-inline d-sm-block float-right">
                                <icon
                                    class="move-icon"
                                    name="arrows"
                                    scale="1.75"
                                />
                            </div>
                        </student-card>
                    </draggable>
                    <div class="invisible"/>
                </div>
            </div>
        </div>
        <slot/>
    </b-card>
</template>

<script>
import progressBar from '@/components/assets/ProgressBar.vue'
import numberBadge from '@/components/assets/NumberBadge.vue'
import studentCard from '@/components/assignment/StudentCard.vue'
import draggable from 'vuedraggable'

export default {
    components: {
        progressBar,
        numberBadge,
        studentCard,
        draggable,
    },
    props: {
        assignment: {
            required: true,
        },
        journal: {
            required: true,
        },
    },
    data () {
        return {
            editJournal: false,
        }
    },
    computed: {
        numMarkingNeeded () {
            return this.journal.stats ? this.journal.stats.submitted - this.journal.stats.graded : 0
        },
        journalAuthors () {
            if (this.assignment.is_group_assignment) {
                return this.journal.authors.map(a => a.user.full_name).join(', ')
            }

            return this.journal.authors.map(a => a.user.username).join(', ')
        },
        groups () {
            const groups = []
            this.journal.authors.forEach((student) => {
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
            return this.journal.stats ? this.journal.stats.submitted - this.journal.stats.graded : 0
        },
        unpublished () {
            return this.journal.stats ? this.journal.stats.graded - this.journal.stats.published : 0
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
    methods: {
        log (evt) {
            window.console.log(evt);
        },
    },
}
</script>

<style lang="sass">
@import '~sass/partials/shadows.sass'
@import '~sass/modules/breakpoints.sass'
@import '~sass/modules/colors.sass'

.portrait-wrapper
    position: relative
    min-width: 80px
    height: 70px
    img
        @extend .shadow
        width: 70px
        height: 70px
        border-radius: 50% !important
    .number-badge, .badge
        position: absolute
        right: 0px
        top: 0px
        font-family: 'Roboto Condensed', sans-serif
        font-size: 1em
        border-radius: 5px !important
        border: 1px solid #CCCCCC
        background-color: white
        color: $theme-dark-blue

.student-details
    position: relative
    width: calc(100% - 80px)
    min-height: 70px
    flex-direction: column
    padding: 10px
    .max-one-line
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
