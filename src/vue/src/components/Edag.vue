<!--
    Edag component. Handles the prop connection with parent, as well as any
    functionality involving the list (ie. showing the list,
    passing selected state)

    Example data:
    data () {
        return {
            selected: 2,
            nodes: [
                {
                    type: 'e',
                    text: '',
                    nID: 0,
                    date: new Date()
                },
                {
                    type: 'entry',
                    text: '',
                    id: 1,
                    date: new Date()
                },
                {
                    type: 'entry',
                    text: '',
                    id: 2,
                    date: new Date()
                },
                {
                    type: 'progress',
                    text: '5',
                    id: 3,
                    date: new Date()
                }
            ]
        }
    }
-->

<template>
    <div id="edag-outer">
        <div id="edag-inner" ref="scd">
            <edag-node v-for="(node, index) in this.nodes" @select-node="$emit('select-node', $event)" :index="index" :node="node" :selected="isSelected(index)" :key="node.nID" :upperEdgeStyle="upperEdgeStyle(index)" :lowerEdgeStyle="lowerEdgeStyle(index)"/>
        </div>
    </div>
</template>

<script>
import edagNode from '@/components/EdagNode'

export default {
    props: ['selected', 'nodes', 'edgeStyles'],
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
        'edag-node': edagNode
    }
}
</script>

<style>
#edag-outer {
    overflow: hidden;
    height: 100%;
}
#edag-inner {
    height: 100%;
    overflow-y: scroll;
    overflow-x: hidden;
    padding-right: 25px;
    margin-right: -20px; /* Increase/decrease this value for cross-browser compatibility */
}

#edag-div::-webkit-scrollbar {
    display: none;
}
</style>
