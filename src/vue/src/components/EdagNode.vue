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
            <edag-node-date :date="node.date" :selected="selected"/>
        </b-col>
        <b-col cols="4" class="d-flex align-items-center justify-content-center">
            <div style="width: 0.5em; height: 5em; background-color: var(--theme-light-grey)" :style="{ height: this.lineHeight }"/> <!-- grey line -->
            <edag-node-circle style="position: absolute" :type="node.type" :text="node.text" :selected="selected"></edag-node-circle>
        </b-col>
    </b-row>
</template>

<script>
import edagNodeCircle from '@/components/EdagNodeCircle.vue'
import edagNodeDate from '@/components/EdagNodeDate.vue'

export default {
    props: ['node', 'selected'],
    computed: {
        lineHeight () {
            return (this.selected) ? '7em' : '5em'
        }
    },
    components: {
        'edag-node-date': edagNodeDate,
        'edag-node-circle': edagNodeCircle
    }
}
</script>

<style>
/*  */
</style>
