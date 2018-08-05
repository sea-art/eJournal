<!--
    Edag component. Handles the prop connection with parent, as well as any
    functionality involving the list (ie. showing the list,
    passing selected state)
-->

<template>
    <div class="edag-container">
        <b-collapse id="edag-outer">
            <div id="edag-inner" ref="scd">
                <div v-if="$root.lgMax()" v-b-toggle.edag-outer target="edag-outer" aria-expanded="false" aria-controls="edag-outer">
                    <edag-node
                        v-for="(node, index) in this.nodes"
                        @select-node="$emit('select-node', $event)"
                        :index="index"
                        :node="node"
                        :selected="isSelected(index)"
                        :isInEditFormatPage="isInEditFormatPage"
                        :key="node.nID"
                        :upperEdgeStyle="upperEdgeStyle(index)"
                        :lowerEdgeStyle="lowerEdgeStyle(index)"/>
                </div>
                <edag-node
                    v-else
                    v-for="(node, index) in this.nodes"
                    @select-node="$emit('select-node', $event)"
                    :index="index"
                    :node="node"
                    :selected="isSelected(index)"
                    :isInEditFormatPage="isInEditFormatPage"
                    :key="node.nID"
                    :upperEdgeStyle="upperEdgeStyle(index)"
                    :lowerEdgeStyle="lowerEdgeStyle(index)"/>
            </div>
        </b-collapse>

        <div v-b-toggle.edag-outer target="edag-outer" aria-expanded="false" aria-controls="edag-outer" id="edag-toggle">
            <span class="edag-outer__icon edag-outer__icon--open">
                    <icon class="collapse-icon" name="list-ul" scale="1.75"/>
            </span>
            <span class="edag-outer__icon edag-outer__icon--close">
                    <icon class="collapse-icon" name="caret-up" scale="1.75"/>
            </span>
        </div>
    </div>
</template>

<script>
import edagNode from '@/components/edag/EdagNode.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['selected', 'nodes', 'edgeStyles', 'isInEditFormatPage'],
    methods: {
        isSelected (id) {
            return id === this.selected
        },
        upperEdgeStyle (nodeIndex) {
            if (nodeIndex === 0) {
                return {'background-color': 'white'}
            }
            if (!this.edgeStyles || !this.edgeStyles[nodeIndex - 1]) {
                return {}
            }
            return this.edgeStyles[nodeIndex - 1]
        },
        lowerEdgeStyle (nodeIndex) {
            if (nodeIndex === this.nodes.length - 1) {
                return {'background-color': 'white'}
            }
            if (!this.edgeStyles || !this.edgeStyles[nodeIndex]) {
                return {}
            }
            return this.edgeStyles[nodeIndex]
        }
    },
    components: {
        'edag-node': edagNode,
        'icon': icon
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/modules/breakpoints.sass'

.edag-container
    @include lg-max
        text-align: center
    @include xl
        height: 100%

#edag-inner::-webkit-scrollbar
    display: none

#edag-outer
    overflow: hidden
    height: 100%
    @include lg-max
        background-color: white

@include xl
    #edag-outer[style]
        display: block !important

#edag-inner
    height: 100%
    overflow-y: scroll
    overflow-x: hidden
    padding-right: 40px
    margin-right: -20px
    @include lg-max
        height: 50vh

@include lg-max
    /* Handles changing of the button icon. */
    [aria-expanded="false"] .edag-outer__icon--open
        display: block
        text-align: center

    [aria-expanded="false"] .edag-outer__icon--close
        display: none
        text-align: center

    [aria-expanded="true"] .edag-outer__icon--open
        display: none
        text-align: center

    [aria-expanded="true"] .edag-outer__icon--close
        display: block
        text-align: center

    #edag-toggle
        border: 0px
        padding: 10px 0px
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
