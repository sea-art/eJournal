<!--
    Timeline component. Handles the prop connection with parent, as well as any
    functionality involving the list (ie. showing the list,
    passing selected state)
-->

<template>
    <div class="timeline-container">
        <b-collapse id="timeline-outer">
            <div class="timeline-inner" ref="scd">
                <div v-if="$root.lgMax()" v-b-toggle.timeline-outer target="timeline-outer" aria-expanded="false" aria-controls="timeline-outer">
                    <timeline-node
                        @select-node="$emit('select-node', $event)"
                        :index="-1"
                        :node="{
                            'type': 's'
                        }"
                        :selected="isSelected(-1)"
                        :edit="edit"/>
                    <timeline-node
                        v-for="(node, index) in this.nodes"
                        @select-node="$emit('select-node', $event)"
                        :index="index"
                        :node="node"
                        :selected="isSelected(index)"
                        :edit="edit"
                        :key="node.id"/>
                    <timeline-node
                        v-if="edit"
                        @select-node="$emit('add-node')"
                        :node="{
                            'type': 'a'
                        }"
                        :edit="edit"/>
                    <timeline-node
                        @select-node="$emit('select-node', $event)"
                        :index="nodes.length"
                        :last="true"
                        :node="{
                            'type': 'n'
                        }"
                        :selected="isSelected(nodes.length)"
                        :edit="edit"/>
                </div>
                <div v-else>
                    <timeline-node
                        @select-node="$emit('select-node', $event)"
                        :index="-1"
                        :node="{
                            'type': 's'
                        }"
                        :selected="isSelected(-1)"
                        :edit="edit"/>
                    <timeline-node
                        v-for="(node, index) in this.nodes"
                        @select-node="$emit('select-node', $event)"
                        :index="index"
                        :node="node"
                        :selected="isSelected(index)"
                        :edit="edit"
                        :key="node.id"/>
                    <timeline-node
                        v-if="edit"
                        @select-node="$emit('add-node')"
                        :node="{
                            'type': 'a'
                        }"
                        :edit="edit"/>
                    <timeline-node
                        @select-node="$emit('select-node', $event)"
                        :index="nodes.length"
                        :last="true"
                        :node="{
                            'type': 'n'
                        }"
                        :selected="isSelected(nodes.length)"
                        :edit="edit"/>
                </div>
            </div>
        </b-collapse>

        <div
            v-b-toggle.timeline-outer
            target="timeline-outer"
            aria-expanded="false"
            aria-controls="timeline-outer"
            id="timeline-toggle">
            <span class="timeline-outer__icon timeline-outer__icon--open">
                    <icon class="collapse-icon" name="list-ul" scale="1.75"/>
            </span>
            <span class="timeline-outer__icon timeline-outer__icon--close">
                    <icon class="collapse-icon" name="caret-up" scale="1.75"/>
            </span>
        </div>
    </div>
</template>

<script>
import timelineNode from '@/components/timeline/TimelineNode.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['selected', 'nodes', 'edit'],
    methods: {
        isSelected (id) {
            return id === this.selected
        }
    },
    components: {
        'timeline-node': timelineNode,
        icon
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/modules/breakpoints.sass'

.timeline-container
    @include lg-max
        text-align: center
    @include xl
        height: 100%

.timeline-inner::-webkit-scrollbar
    display: none

#timeline-outer
    overflow: hidden
    height: 100%

@include xl
    #timeline-outer[style]
        display: block !important

.timeline-inner
    height: 100%
    overflow-y: scroll
    overflow-x: hidden
    padding-right: 40px
    margin-right: -20px
    @include lg-max
        height: 50vh

@include lg-max
    /* Handles changing of the button icon. */
    [aria-expanded="false"] .timeline-outer__icon--open
        display: block
        text-align: center

    [aria-expanded="false"] .timeline-outer__icon--close
        display: none
        text-align: center

    [aria-expanded="true"] .timeline-outer__icon--open
        display: none
        text-align: center

    [aria-expanded="true"] .timeline-outer__icon--close
        display: block
        text-align: center

    #timeline-toggle
        border: 0px
        padding: 10px 0px
        border-radius: 40px !important
        background-color: $theme-blue !important
        &:hover
            background-color: $theme-blue !important
            cursor: pointer
        .collapse-icon
            display: block
            margin-left: auto
            margin-right: auto
            fill: white
</style>
