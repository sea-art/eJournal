<!--
    Component representing a node in the Timeline.
    Handles the compositing of circle and date subcomponents, its own style
    depending on state given by parent, and passes relevant parts of the state
    to the subcomponents.
-->

<template>
    <b-row class="node-container">
        <b-col
            cols="8"
            class="d-flex h-100 align-items-center"
        >
            <timeline-node-info
                :node="node"
                :selected="selected"
            />
        </b-col>
        <b-col
            cols="4"
            class="d-flex h-100 align-items-center justify-content-center"
        >
            <div
                :class="timeLineClass"
                class="time-line"
            />
            <timeline-node-circle
                :node="node"
                :selected="selected"
                :edit="edit"
                class="position-absolute"
                @click.native="$emit('select-node', index)"
            />
        </b-col>
    </b-row>
</template>

<script>
import timelineNodeCircle from '@/components/timeline/TimelineNodeCircle.vue'
import timelineNodeInfo from '@/components/timeline/TimelineNodeInfo.vue'

export default {
    components: {
        timelineNodeInfo,
        timelineNodeCircle,
    },
    props: ['node', 'selected', 'index', 'last', 'edit'],
    computed: {
        timeLineClass () {
            return {
                top: this.index === -1,
                bottom: this.last,
            }
        },
    },
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.node-container
    height: 100px
    .time-line
        position: absolute
        width: 5px
        background-color: $theme-dark-grey
        height: 100px
        &.top
            height: 50px
            top: 50px
        &.bottom
            height: 50px
            bottom: 50px
</style>
