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
    <div class="edag-container">
        <b-collapse id="edag-outer">
            <div id="edag-inner" ref="scd">
                <edag-node v-for="(node, index) in this.nodes" @select-node="$emit('select-node', $event)" :index="index" :node="node" :selected="isSelected(index)" :key="node.nID" :upperEdgeStyle="upperEdgeStyle(index)" :lowerEdgeStyle="lowerEdgeStyle(index)"/>
            </div>
        </b-collapse>

        <b-card v-b-toggle.edag-outer target="edag-outer" aria-expanded="false" aria-controls="edag-outer" class="edag-toggle">
            <span class="edag-outer__icon edag-outer__icon--open">
                <b>Show Timeline</b>
            </span>
            <span class="edag-outer__icon edag-outer__icon--close">
                Hide Timeline
            </span>
        </b-card>
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
@media (min-width: 1200px) {
    .edag-container {
        height: 100%;
    }

    #edag-outer[style] {
        display: block !important;
    }

    #edag-outer {
        overflow: hidden;
        height: 100%;
    }

    #edag-inner {
        height: 100%;
        overflow-y: scroll;
        overflow-x: hidden;
        padding-right: 40px;
        margin-right: -20px;
    }
}

@media (max-width: 1200px) {
    /* Handles changing of the button text. */
    [aria-expanded="false"] .edag-outer__icon--open {
        display: block;
        text-align: center;
    }

    [aria-expanded="false"] .edag-outer__icon--close {
        display: none;
        text-align: center;
    }

    [aria-expanded="true"] .edag-outer__icon--open {
        display: none;
        text-align: center;
    }

    [aria-expanded="true"] .edag-outer__icon--close {
        display: block;
        text-align: center;
    }

    .edag-toggle {
        margin-top: 10px;
        width: 100%;
        border-color: var(--theme-dark-blue);
    }

    .edag-container {
        text-align: center;
    }
}

#edag-inner::-webkit-scrollbar {
    display: none;
}
</style>
