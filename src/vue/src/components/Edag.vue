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
                    type: 'entry',
                    text: '',
                    id: 0,
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
    <div id="edag-div" class="h-100 mh-100">
        <edag-node v-for="node in this.nodes" @click.native="$emit('select-node', node.id)" :node="node" :selected="isSelected(node.id)" :key="node.id"/>
    </div>
</template>

<script>
import edagNode from '@/components/EdagNode'

export default {
    props: ['selected', 'nodes'],
    methods: {
        isSelected (id) {
            return id === this.selected
        }
    },
    components: {
        'edag-node': edagNode
    }
}
</script>

<style>
#edag-div {
    overflow-y: scroll;
}
</style>
