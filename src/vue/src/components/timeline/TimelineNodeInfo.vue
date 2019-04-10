<!--
    Mini component representing the date for a node in the Timeline.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span class="node-info" :class="{'selected': this.selected}">
        <span v-if="nodeTitle" class="node-title">
            <icon
                v-if="new Date(nodeDate) > new Date()"
                name="calendar"
                class="mb-1 mr-1"
                v-b-tooltip.hover
                title="Upcoming deadline"/>
            {{ nodeTitle }}<br/>
        </span>

        <span v-if="nodeDate" class="node-date" v-b-tooltip.hover :title="deadlineRange">
            {{ $root.beautifyDate(nodeDate) }}
        </span>
    </span>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['node', 'selected'],
    computed: {
        nodeTitle () {
            if (this.node.entry) {
                return this.node.entry.template.name
            } else if (this.node.template) {
                return this.node.template.name
            } else if (this.node.target) {
                return 'Point target'
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
            var unlockDate = this.$root.beautifyDate(this.node.unlock_date)
            var lockDate = this.$root.beautifyDate(this.node.lock_date)

            if (unlockDate && lockDate) {
                return `Available from ${unlockDate} until ${lockDate}`
            } else if (unlockDate) {
                return `Available from ${unlockDate}`
            } else if (lockDate) {
                return `Available until ${lockDate}`
            }

            return ''
        }
    },
    components: {
        icon
    }
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
