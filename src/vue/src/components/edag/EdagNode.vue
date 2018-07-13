<!--
    Component representing a node in the EDAG.
    Handles the compositing of circle and date subcomponents, its own style
    depending on state given by parent, and passes relevant parts of the state
    to the subcomponents.
-->

<template>
    <b-row>
        <b-col cols="4" sm="1"/>
        <b-col cols="4" sm="5" class="d-flex align-items-center justify-content-center">
            <edag-node-date :date="node.deadline" :selected="selected"/>
        </b-col>
        <b-col cols="4" sm="5" class="d-flex align-items-center justify-content-center">
            <div>
                <!-- TODO Please fix no style in line, variable #EEEEEE (Theme light grey not dry) -->
                <div style="width: 0.5em; height: 3em; background-color: #EEEEEE" :style="upperEdgeStyle"/> <!-- grey line -->
                <div style="width: 0.5em; height: 3em; background-color: #EEEEEE" :style="lowerEdgeStyle"/> <!-- grey line -->
            </div>
            <edag-node-circle  v-if="node.type == 'a'" @click.native="$emit('select-node', index)" style="position: absolute" :type="node.type" :selected="selected" :entrystate="'addNode'"></edag-node-circle>
            <edag-node-circle v-else @click.native="$emit('select-node', index)" style="position: absolute" :type="node.type" :text="node.target" :selected="selected" :entrystate="entryState()"></edag-node-circle>
        </b-col>
        <b-col cols="4" sm="1"/>
    </b-row>
</template>

<script>
import edagNodeCircle from '@/components/edag/EdagNodeCircle.vue'
import edagNodeDate from '@/components/edag/EdagNodeDate.vue'

export default {
    props: ['node', 'selected', 'upperEdgeStyle', 'lowerEdgeStyle', 'index', 'isInEditFormatPage'],
    components: {
        'edag-node-date': edagNodeDate,
        'edag-node-circle': edagNodeCircle
    },
    computed: {
        deadlineHasPassed () {
            var currentDate = new Date()
            var deadline = new Date(this.node.deadline)

            return currentDate > deadline
        }
    },
    methods: {
        entryState () {
            if (this.isInEditFormatPage) {
                return ''
            }
            if (this.node.type === 'p' || this.node.type === 'a') {
                return ''
            }

            var entry = this.node.entry
            var isGrader = this.$root.canPublishAssignmentGrades()

            if (entry && entry.published) {
                return 'graded'
            }

            if (!entry && this.deadlineHasPassed) {
                return 'failed'
            }
            if (!entry && !this.deadlineHasPassed) {
                return 'empty'
            }

            if (!isGrader && entry && !entry.published && this.deadlineHasPassed) {
                return 'grading'
            }
            if (!isGrader && entry && !entry.published && !this.deadlineHasPassed) {
                return ''
            }

            if (isGrader && entry && !entry.published) {
                return 'needsgrading'
            }

            return ''
        }
    }
}
</script>
