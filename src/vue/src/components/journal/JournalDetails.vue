<template>
    <!-- TODO GROUPS ENGEL: Use APIs -->
    <b-card
        class="journal-details"
        :class="$root.getBorderClass($route.params.cID)">
        <img
            :src="journal.image"
            class="journal-image no-hover"
        />
        <span class="edit-journal">
            <icon
                v-if="assignment.is_group_assignment"
                name="edit"
                @click="showEditJournalModal"
            />
            Edit
        </span>
        <progress-bar
            :currentPoints="journal.stats.acquired_points"
            :totalPoints="assignment.points_possible"
            :comparePoints="assignment && assignment.stats ? assignment.stats.average_points : -1"
            :bonusPoints="journal.bonus_points"
        />
        <div
            class="members"
        >
            <div v-if="assignment.is_group_assignment">
                <icon
                    name="lock"
                    class="lock-members-icon"
                    :class="{
                        'fill-red': journal.locked,
                        'fill-grey': !journal.locked
                    }"
                />
                <b class="member-count">
                    Members ({{ journal.authors.length }}/{{ journal.author_limit }})
                </b>
                <div
                    class="member"
                    v-for="author in journal.authors.map(a => a.user)"
                    :key="`journal-member-${author.username}`"
                >
                    <icon
                        name="sign-out"
                        class="float-right trash-icon"
                    />
                    <b class="max-one-line">
                        {{ author.full_name }}
                    </b>
                    <span class="max-one-line">
                        {{ author.username }}
                    </span>
                </div>
            </div>
            <div v-else>
                <b class="max-one-line">
                    {{ journalName }}
                </b>
                <span class="max-one-line">
                    {{ journalAuthorUsername }}
                </span>
            </div>
        </div>
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
            default: null,
            required: true,
        },
        journal: {
            required: true,
        },
        listView: {
            default: false,
        },
        editView: {
            default: false,
        },
    },
    computed: {
        journalAuthorUsername () {
            if (this.journal.authors && this.journal.authors.length > 0) {
                return this.journal.authors[0].username
            }
            return ''
        },
        journalName () {
            return this.journal.name ? this.journal.name : 'Empty journal'
        },
    },
    methods: {
        showEditJournalModal () {
            this.$refs.editJournalModal.show()
        }
    },
}
</script>

<style lang="sass">
@import '~sass/partials/shadows.sass'
@import '~sass/modules/breakpoints.sass'
@import '~sass/modules/colors.sass'

.journal-details
    .card-body
        padding-top: 45px
    .journal-image
        @extend .shadow
        position: absolute
        width: 70px
        height: 70px
        left: 50%
        top: -25px
        margin-left: -35px
        border-radius: 50% !important
        background-color: white
    .edit-journal
        position: absolute
        right: 10px
        top: 5px
        color: grey
        svg
            margin-top: -2px
            fill: grey !important
        &:hover:not(.no-hover)
            cursor: pointer
            color: darken(grey, 20)
            svg
                fill: darken(grey, 20) !important
    .members
        margin-top: 10px
        .member
            padding: 5px
            border-style: solid
            border-color: $theme-dark-grey
            border-width: 1px 0px
            .trash-icon
                margin-top: 3px
            .max-one-line
                width: calc(100% - 20px)
        .lock-members-icon
            float: right
            margin-top: 3px
            margin-right: 9px
            svg
                fill: red
    .temp
        display: block
        width: 100%
        min-height: 70px
        margin-bottom: 10px
        .max-one-line
            width: calc(100% - 70px)
        &.list-view
            padding-left: 40px
        @include sm-max
            align-items: flex-end

</style>
