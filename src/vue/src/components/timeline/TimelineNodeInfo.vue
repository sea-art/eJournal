<!--
    Mini component representing the date for a node in the Timeline.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span
        :class="{'selected': selected}"
        class="node-info"
    >
        <span
            v-if="nodeTitle"
            class="node-title"
        >
            <icon
                v-if="new Date(nodeDate) > new Date()"
                v-b-tooltip.hover
                name="calendar"
                class="mb-1 mr-1"
                title="Upcoming deadline"
            />
            {{ nodeTitle }}<br/>
        </span>

        <span
            v-if="nodeDate"
            v-b-tooltip.hover
            :title="deadlineRange"
            class="node-date"
        >
            {{ $root.beautifyDate(nodeDate) }}
        </span>
    </span>
</template>

<script>
export default {
    props: ['node', 'selected'],
    computed: {
        nodeTitle () {
            if (this.node.type === 'e') { // Entry
                return this.node.entry.template.name
            } else if (this.node.type === 'd') { // Entry deadline
                return this.node.template.name
            } else if (this.node.type === 'p') { // Progress node
                return 'Progress goal'
            } else {
                return null
            }
        },
        nodeDate () {
            if (this.node.entry && this.node.entry.creation_date) {
                return this.node.entry.creation_date
            } else if (this.node.due_date) {
                return this.node.due_date
            } else {
                return null
            }
        },
        deadlineRange () {
            const unlockDate = this.$root.beautifyDate(this.node.unlock_date)
            const lockDate = this.$root.beautifyDate(this.node.lock_date)

            if (unlockDate && lockDate) {
                return `Available from ${unlockDate} until ${lockDate}`
            } else if (unlockDate) {
                return `Available from ${unlockDate}`
            } else if (lockDate) {
                return `Available until ${lockDate}`
            }

            return ''
        },
    },
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.node-info
    text-align: right
    width: 100%
    user-select: none
    &.selected
        cursor: auto
        opacity: 1
    &:not(.selected)
        opacity: 0.5
    .node-title
        font-weight: bold
        color: grey
    .node-date
        font-family: 'Roboto Condensed'
        font-size: 0.9em
        color: grey
</style>
