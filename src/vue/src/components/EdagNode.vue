<!--
    Component representing a node in the EDAG.
    Handles the compositing of circle and date subcomponents, its own style
    depending on state given by parent, and passes relevant parts of the state
    to the subcomponents.
-->

<template>
    <b-row>
        <b-col cols="4"/>
        <b-col cols="4" class="d-flex align-items-center justify-content-center">
            <edag-node-date :date="node.deadline" :selected="selected"/>
        </b-col>
        <b-col cols="4" class="d-flex align-items-center justify-content-center">
            <div>
                <div style="width: 0.5em; height: 3em; background-color: var(--theme-light-grey)" :style="upperEdgeStyle"/> <!-- grey line -->
                <div style="width: 0.5em; height: 3em; background-color: var(--theme-light-grey)" :style="lowerEdgeStyle"/> <!-- grey line -->
            </div>
            <edag-node-circle @click.native="$emit('select-node', index)" style="position: absolute" :type="node.type" :text="node.text" :selected="selected"></edag-node-circle>
        </b-col>
    </b-row>
</template>

<script>
import edagNodeCircle from '@/components/EdagNodeCircle.vue'
import edagNodeDate from '@/components/EdagNodeDate.vue'

export default {
    props: ['node', 'selected', 'upperEdgeStyle', 'lowerEdgeStyle', 'index'],
    components: {
        'edag-node-date': edagNodeDate,
        'edag-node-circle': edagNodeCircle
    }
}
</script>

<style>
/*  */
</style>
