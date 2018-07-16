<!--
    Mini component representing the circle for a node in the EDAG.
    Handles its own style depending on a state given by parent.
-->

<template>
    <div class="edag-node-circle-border">
        <div class="edag-node-circle d-flex align-items-center justify-content-center" :class="classObject">
            <div v-if="this.entrystate === 'empty'" class="edag-node-circle-inner" :class="classObject"></div>
            <icon v-else-if="this.entrystate != ''" :name="iconName" class="edag-node-circle-icon fill-white" :scale="iconScale"/>
            <div v-else class="text-white">{{ text }}</div>
        </div>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['type', 'text', 'selected', 'entrystate'],
    computed: {
        classObject () {
            return {
                'enc-entry': this.type === 'e',
                'enc-deadline': this.type === 'd',
                'enc-progress': this.type === 'p',
                'enc-add': this.type === 'a',
                'enc-selected': this.selected
            }
        },
        iconName () {
            switch (this.entrystate) {
            case 'grading':
                return 'hourglass-half'
            case 'graded':
                return 'check'
            case 'fulfilled':
                return 'check'
            case 'failed':
                return 'times'
            case 'needsgrading':
                return 'exclamation'
            case 'addNode':
                return 'plus'
            default:
                return ''
            }
        },
        iconScale () {
            if (this.entrystate === 'addNode') {
                if (this.selected) {
                    return '2'
                } else {
                    return '1'
                }
            }
            if (this.selected) {
                return '2.5'
            } else {
                return '1.5'
            }
        }
    },
    components: {
        'icon': icon
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
.text-white
    color: white

.fill-white
    fill: white

.edag-node-circle-border
    border-radius: 50% !important
    background-color: white
    padding: 5px

.edag-node-circle
    width: 55px
    height: 55px
    border-radius: 50% !important
    &.enc-selected
        width: 65px
        height: 65px
    &.enc-add
        width: 45px
        height: 45px
    &.enc-selected.enc-add
        width: 55px
        height: 55px
    &.enc-entry
        background-color: $theme-medium-grey
    &.enc-entry:hover
        background-color: $theme-dark-grey
    &.enc-entry.enc-selected
        background-color: $theme-dark-grey
    &.enc-deadline
        background-color: $theme-change-selected
    &.enc-deadline:hover
        background-color: $theme-change-hover
    &.enc-deadline.enc-selected
        background-color: $theme-change-hover
    &.enc-progress
        background-color: $theme-negative-selected
    &.enc-progress:hover
        background-color: $theme-red
    &.enc-progress.enc-selected
        background-color: $theme-red
    &.enc-add
        background-color: $theme-blue
    &.enc-add:hover
        background-color: $theme-dark-blue
    &.enc-add.enc-selected
        background-color: $theme-dark-blue

.edag-node-circle-inner
    width: 35px
    height: 35px
    background-color: white
    border-radius: 50% !important
    &.enc-selected,
        width: 45px
        height: 45px
</style>
